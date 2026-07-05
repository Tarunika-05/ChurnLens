from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/churn_analytics"
    data_raw_path: str = "data/raw/Telco-Customer-Churn.csv"
    data_processed_path: str = "data/processed/churn_cleaned.csv"
    model_path: str = "models/best_model.pkl"
    predictions_path: str = "models/predictions.csv"
    metrics_path: str = "models/model_metrics.json"
    log_level: str = "INFO"
    environment: str = "development"
    random_state: int = 42
    test_size: float = 0.2

    class Config:
        env_file = ".env"


settings = Settings()

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / settings.data_raw_path
DATA_PROCESSED = ROOT / settings.data_processed_path
PREDICTIONS_PATH = ROOT / settings.predictions_path
MODEL_PATH = ROOT / settings.model_path
METRICS_PATH = ROOT / settings.metrics_path
IMAGES_DIR = ROOT / "images"
REPORTS_DIR = ROOT / "reports"

RANDOM_STATE = settings.random_state
TEST_SIZE = settings.test_size
