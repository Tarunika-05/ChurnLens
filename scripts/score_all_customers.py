"""Score all customers for Power BI dashboard (not just test holdout)."""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import DATA_PROCESSED, MODEL_PATH, settings
from src.features import add_engineered_features, get_model_features
from src.logger import setup_logging

DASHBOARD_DATA = ROOT / "dashboard" / "dashboard_data.csv"

def main() -> None:
    logger = setup_logging(settings.log_level)
    try:
        df = add_engineered_features(pd.read_csv(DATA_PROCESSED))
        model = joblib.load(MODEL_PATH)
        features = get_model_features()

        probabilities = model.predict_proba(df[features])[:, 1]
        dashboard_df = df.copy()
        dashboard_df["churn_probability"] = probabilities
        dashboard_df["predicted_churn"] = (probabilities >= 0.5).astype(int)
        dashboard_df["risk_tier"] = pd.cut(
            probabilities,
            bins=[-0.01, 0.4, 0.7, 1.0],
            labels=["Low", "Medium", "High"],
        )

        DASHBOARD_DATA.parent.mkdir(parents=True, exist_ok=True)
        dashboard_df.to_csv(DASHBOARD_DATA, index=False)
        logger.info(f"Saved {len(dashboard_df)} rows to {DASHBOARD_DATA}")
    except FileNotFoundError as e:
        logger.error(f"Required file not found. Ensure pipeline has been run. Details: {e}")
    except Exception as e:
        logger.error(f"Error during customer scoring: {e}")


if __name__ == "__main__":
    main()
