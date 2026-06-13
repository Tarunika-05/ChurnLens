"""Tests for ML models."""
import pandas as pd
import pytest
from src.ml_models import train_models
from src.features import add_engineered_features

def test_train_models_missing_columns(sample_clean_data):
    """Test that PipelineError is raised if required columns are missing."""
    from src.exceptions import PipelineError
    
    # Drop a required feature
    df = add_engineered_features(sample_clean_data)
    df = df.drop("tenure", axis=1)
    
    with pytest.raises(PipelineError, match="Missing required columns"):
        train_models(df)
