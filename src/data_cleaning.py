"""Data cleaning utilities for the IBM Telco Customer Churn dataset."""

from __future__ import annotations

import pandas as pd

from src.exceptions import DataLoadError


def load_raw_data(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError as e:
        raise DataLoadError(f"Raw data file not found at {path}") from e
    except Exception as e:
        raise DataLoadError(f"Failed to load raw data: {e!s}") from e


def build_quality_report(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    def missing_total_charges(df: pd.DataFrame) -> int:
        if "TotalCharges" not in df.columns:
            return 0
        series = df["TotalCharges"]
        if pd.api.types.is_numeric_dtype(series):
            return int(series.isna().sum())
        return int((series.astype(str).str.strip() == "").sum())

    rows = [
        ("Total rows", len(before), len(after)),
        (
            "Duplicate customer IDs",
            int(before["customerID"].duplicated().sum()),
            int(after["customerID"].duplicated().sum()),
        ),
        ("Missing TotalCharges", missing_total_charges(before), missing_total_charges(after)),
        (
            "Invalid churn values",
            int((~before["Churn"].isin(["Yes", "No"])).sum()),
            int((~after["Churn"].isin(["Yes", "No"])).sum()),
        ),
        ("Negative tenure", int((before["tenure"] < 0).sum()), int((after["tenure"] < 0).sum())),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Before", "After"])


from src.exceptions import DataValidationError


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required_cols = [
        "customerID",
        "TotalCharges",
        "MonthlyCharges",
        "tenure",
        "SeniorCitizen",
        "Churn",
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise DataValidationError(f"Missing required columns: {missing_cols}")

    before = df.copy()
    cleaned = df.copy()

    try:
        cleaned = cleaned.drop_duplicates(subset=["customerID"], keep="first")
        cleaned["TotalCharges"] = pd.to_numeric(cleaned["TotalCharges"], errors="coerce")
        cleaned.loc[cleaned["tenure"] == 0, "TotalCharges"] = cleaned.loc[
            cleaned["tenure"] == 0, "MonthlyCharges"
        ]
        cleaned["TotalCharges"] = cleaned["TotalCharges"].fillna(cleaned["MonthlyCharges"])
        cleaned["SeniorCitizen"] = cleaned["SeniorCitizen"].astype(int)
        cleaned["tenure"] = cleaned["tenure"].astype(int)
        cleaned["MonthlyCharges"] = cleaned["MonthlyCharges"].astype(float)
        cleaned["TotalCharges"] = cleaned["TotalCharges"].astype(float)
        cleaned = cleaned[cleaned["Churn"].isin(["Yes", "No"])]
        cleaned = cleaned[cleaned["tenure"] >= 0]
    except Exception as e:
        raise DataValidationError(f"Failed to clean data: {e!s}") from e

    report = build_quality_report(before, cleaned)
    return cleaned, report


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    rows = []
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        rows.append(
            {
                "column": col,
                "q1": round(q1, 2),
                "q3": round(q3, 2),
                "lower_fence": round(lower, 2),
                "upper_fence": round(upper, 2),
                "outlier_count": int(outliers),
                "action": "Retained — likely valid high-value customers",
            }
        )
    return pd.DataFrame(rows)
