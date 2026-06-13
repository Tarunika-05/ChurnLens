"""Run end-to-end data processing, modeling, and artifact generation."""

from __future__ import annotations

import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import (
    DATA_PROCESSED,
    DATA_RAW,
    IMAGES_DIR,
    METRICS_PATH,
    MODEL_PATH,
    PREDICTIONS_PATH,
    REPORTS_DIR,
)
from src.data_cleaning import clean_data, load_raw_data, outlier_summary
from src.features import add_engineered_features, get_model_features
from src.ml_models import extract_feature_importance, save_metrics, train_models
from src.explainability import get_shap_explainer, global_shap_summary
from src.statistical_tests import run_all_significance_tests


from src.logger import log_step, setup_logging
from src.config import settings

@log_step("Ensure Directories")
def ensure_directories() -> None:
    for path in [DATA_PROCESSED.parent, MODEL_PATH.parent, IMAGES_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


@log_step("Build Business Summary")
def build_business_summary(df: pd.DataFrame) -> dict:
    churned = df[df["churn_flag"]]
    return {
        "total_customers": int(len(df)),
        "active_customers": int((~df["churn_flag"]).sum()),
        "churned_customers": int(df["churn_flag"].sum()),
        "churn_rate_pct": round(df["churn_flag"].mean() * 100, 2),
        "monthly_revenue": round(df.loc[~df["churn_flag"], "MonthlyCharges"].sum(), 2),
        "revenue_lost_monthly": round(churned["MonthlyCharges"].sum(), 2),
        "avg_clv": round(df["estimated_clv"].mean(), 2),
    }


@log_step("Save EDA Charts")
def save_eda_charts(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5))
    churn_counts = df["Churn"].value_counts()
    sns.barplot(x=churn_counts.index, y=churn_counts.values, palette=["#2E86AB", "#E94F37"], ax=ax)
    ax.set_title("Customer Churn Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Customers")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_distribution.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    contract_churn = (
        df.groupby("Contract")["churn_flag"].mean().sort_values(ascending=False) * 100
    )
    sns.barplot(x=contract_churn.index, y=contract_churn.values, palette="Reds_r", ax=ax)
    ax.set_title("Churn Rate by Contract Type")
    ax.set_xlabel("Contract")
    ax.set_ylabel("Churn Rate (%)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_by_contract.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    tenure_churn = df.groupby("tenure_bucket")["churn_flag"].mean().reindex(
        ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
    ) * 100
    sns.barplot(x=tenure_churn.index, y=tenure_churn.values, palette="OrRd", ax=ax)
    ax.set_title("Churn Rate by Tenure Group")
    ax.set_xlabel("Tenure Bucket")
    ax.set_ylabel("Churn Rate (%)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_by_tenure.png", dpi=150)
    plt.close(fig)


@log_step("Save Feature Importance Chart")
def save_feature_importance_chart(model, df: pd.DataFrame) -> None:
    importance = extract_feature_importance(model, df[get_model_features()])
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(
        data=importance.head(12),
        y="feature",
        x="importance",
        palette="viridis",
        ax=ax,
    )
    ax.set_title("Top Churn Drivers (Best Model)")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "feature_importance.png", dpi=150)
    plt.close(fig)
    importance.to_csv(REPORTS_DIR / "feature_importance.csv", index=False)


@log_step("Save Architecture Diagram")
def save_architecture_diagram() -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    boxes = [
        ("Raw CSV", 0.05, 0.55),
        ("Cleaning\nNotebook", 0.22, 0.55),
        ("Processed CSV", 0.39, 0.55),
        ("PostgreSQL", 0.56, 0.75),
        ("EDA +\nML", 0.56, 0.35),
        ("Power BI", 0.78, 0.55),
        ("Business\nReport", 0.92, 0.55),
    ]
    for label, x, y in boxes:
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F1F8", edgecolor="#2E86AB"),
        )
    arrows = [
        ((0.12, 0.55), (0.17, 0.55)),
        ((0.29, 0.55), (0.34, 0.55)),
        ((0.46, 0.55), (0.51, 0.72)),
        ((0.46, 0.55), (0.51, 0.38)),
        ((0.64, 0.38), (0.72, 0.5)),
        ((0.64, 0.72), (0.72, 0.58)),
        ((0.84, 0.55), (0.88, 0.55)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", color="#555"))
    ax.set_title("Customer Churn Analytics Architecture", fontsize=14, pad=20)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "architecture.png", dpi=150)
    plt.close(fig)


@log_step("Main Pipeline Execution")
def main() -> None:
    logger = setup_logging(settings.log_level)
    logger.info("Starting Customer Churn Analytics Pipeline")
    try:
        ensure_directories()
        raw_df = load_raw_data(DATA_RAW)
        cleaned_df, quality_report = clean_data(raw_df)
        outlier_report = outlier_summary(cleaned_df)
        enriched_df = add_engineered_features(cleaned_df)

        enriched_df.to_csv(DATA_PROCESSED, index=False)
        quality_report.to_csv(REPORTS_DIR / "data_quality_report.csv", index=False)
        outlier_report.to_csv(REPORTS_DIR / "outlier_report.csv", index=False)

        summary = build_business_summary(enriched_df)
        with open(REPORTS_DIR / "business_summary.json", "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)
            
        logger.info("Running statistical significance tests...")
        stats_df = run_all_significance_tests(enriched_df)
        stats_df.to_csv(REPORTS_DIR / "statistical_tests.csv", index=False)

        save_eda_charts(enriched_df)
        best_model, metrics_df, predictions = train_models(enriched_df)
        joblib.dump(best_model, MODEL_PATH)
        save_metrics(metrics_df, METRICS_PATH)
        predictions.to_csv(PREDICTIONS_PATH, index=False)
        save_feature_importance_chart(best_model, enriched_df)
        save_architecture_diagram()

        # Generate SHAP Global Summary
        logger.info("Generating global SHAP summary...")
        features = get_model_features()
        X_background = enriched_df[features].sample(min(100, len(enriched_df)), random_state=settings.random_state)
        explainer, preprocessor = get_shap_explainer(best_model, X_background)
        shap_summary_path = IMAGES_DIR / "shap_summary.png"
        global_shap_summary(explainer, preprocessor, enriched_df[features], features, str(shap_summary_path))

        logger.info("Pipeline complete.")
        logger.info("Business Summary:\n%s", json.dumps(summary, indent=2))
        logger.info("Model Metrics:\n%s", metrics_df.to_string(index=False))
    except Exception as e:
        logger.error("Pipeline failed with error: %s", str(e), exc_info=True)
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
