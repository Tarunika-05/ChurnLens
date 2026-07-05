"""Dependency injection for model loading and data access."""
from functools import lru_cache

import joblib

from src.config import MODEL_PATH
from src.exceptions import ModelLoadError
from src.logger import setup_logging

logger = setup_logging()

@lru_cache
def get_model():
    """Load and cache the trained model."""
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model successfully loaded from {MODEL_PATH}")
        return model
    except FileNotFoundError as e:
        logger.error(f"Model file not found at {MODEL_PATH}. Has the pipeline been run?")
        raise ModelLoadError(f"Model not found at {MODEL_PATH}") from e
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise ModelLoadError(f"Error loading model: {e}") from e

@lru_cache
def get_explainer():
    import pandas as pd

    from src.config import DATA_PROCESSED
    from src.explainability import get_shap_explainer
    from src.features import get_model_features
    try:
        model = get_model()
        df = pd.read_csv(DATA_PROCESSED)
        features = get_model_features()
        X_background = df[features].sample(min(100, len(df)), random_state=42)
        explainer, preprocessor = get_shap_explainer(model, X_background)
        return explainer, preprocessor
    except Exception as e:
        logger.error(f"Error loading SHAP explainer: {e}")
        return None, None
