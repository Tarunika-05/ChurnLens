"""Load cleaned churn data into PostgreSQL."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine

from src.config import DATA_PROCESSED, settings
from src.logger import setup_logging


def main() -> None:
    logger = setup_logging(settings.log_level)
    database_url = settings.database_url
    df = pd.read_csv(DATA_PROCESSED)
    load_df = pd.DataFrame(
        {
            "customer_id": df["customerID"],
            "gender": df["gender"],
            "senior_citizen": df["SeniorCitizen"],
            "partner": df["Partner"],
            "dependents": df["Dependents"],
            "tenure": df["tenure"],
            "phone_service": df["PhoneService"],
            "multiple_lines": df["MultipleLines"],
            "internet_service": df["InternetService"],
            "online_security": df["OnlineSecurity"],
            "online_backup": df["OnlineBackup"],
            "device_protection": df["DeviceProtection"],
            "tech_support": df["TechSupport"],
            "streaming_tv": df["StreamingTV"],
            "streaming_movies": df["StreamingMovies"],
            "contract_type": df["Contract"],
            "paperless_billing": df["PaperlessBilling"],
            "payment_method": df["PaymentMethod"],
            "monthly_charges": df["MonthlyCharges"],
            "total_charges": df["TotalCharges"],
            "churn": df["churn_flag"],
            "tenure_bucket": df["tenure_bucket"],
            "spending_category": df["spending_category"],
            "estimated_clv": df["estimated_clv"],
            "age_group": df["age_group"],
        }
    )
    engine = create_engine(database_url)
    load_df.to_sql("customers", engine, if_exists="replace", index=False)
    logger.info(f"Loaded {len(load_df)} rows into PostgreSQL table 'customers'.")


if __name__ == "__main__":
    main()
