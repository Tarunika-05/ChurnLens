"""Feature engineering for churn modeling and analytics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def tenure_bucket(tenure: int) -> str:
    if tenure <= 12:
        return "0-12 months"
    if tenure <= 24:
        return "12-24 months"
    if tenure <= 48:
        return "24-48 months"
    return "48+ months"


def spending_category(monthly_charge: float, bins: pd.Series | None = None) -> str:
    if bins is None:
        raise ValueError("Spending bins must be provided.")
    if monthly_charge <= bins.iloc[0]:
        return "Low Value"
    if monthly_charge <= bins.iloc[1]:
        return "Medium Value"
    return "High Value"


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    spending_bins = enriched["MonthlyCharges"].quantile([0.33, 0.66])

    enriched["tenure_bucket"] = enriched["tenure"].apply(tenure_bucket)
    enriched["spending_category"] = enriched["MonthlyCharges"].apply(
        lambda value: spending_category(value, spending_bins)
    )
    enriched["estimated_clv"] = enriched["tenure"] * enriched["MonthlyCharges"]
    enriched["has_internet"] = enriched["InternetService"].ne("No")
    enriched["is_month_to_month"] = enriched["Contract"].eq("Month-to-month")
    enriched["churn_flag"] = enriched["Churn"].eq("Yes")
    enriched["age_group"] = np.where(enriched["SeniorCitizen"] == 1, "Senior", "Non-Senior")
    return enriched


def get_model_features() -> list[str]:
    return [
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges",
        "tenure_bucket",
        "spending_category",
        "estimated_clv",
        "has_internet",
        "is_month_to_month",
        "age_group",
    ]
