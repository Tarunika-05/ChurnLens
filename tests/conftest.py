"""Pytest fixtures."""
import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_raw_data():
    """Mock raw data for testing."""
    return pd.DataFrame({
        "customerID": ["001", "002", "003"],
        "gender": ["Male", "Female", "Male"],
        "SeniorCitizen": [0, 1, 0],
        "Partner": ["Yes", "No", "Yes"],
        "Dependents": ["No", "No", "Yes"],
        "tenure": [1, 34, 2],
        "PhoneService": ["Yes", "Yes", "Yes"],
        "MultipleLines": ["No", "Yes", "No"],
        "InternetService": ["DSL", "Fiber optic", "No"],
        "OnlineSecurity": ["No", "Yes", "No internet service"],
        "OnlineBackup": ["Yes", "No", "No internet service"],
        "DeviceProtection": ["No", "Yes", "No internet service"],
        "TechSupport": ["No", "No", "No internet service"],
        "StreamingTV": ["No", "Yes", "No internet service"],
        "StreamingMovies": ["No", "No", "No internet service"],
        "Contract": ["Month-to-month", "One year", "Month-to-month"],
        "PaperlessBilling": ["Yes", "No", "Yes"],
        "PaymentMethod": ["Electronic check", "Mailed check", "Mailed check"],
        "MonthlyCharges": [29.85, 56.95, 20.0],
        "TotalCharges": ["29.85", "1889.5", " "],  # Intentionally string, with one missing
        "Churn": ["No", "No", "Yes"]
    })

@pytest.fixture
def sample_clean_data():
    """Mock clean data for testing features."""
    return pd.DataFrame({
        "customerID": ["001", "002"],
        "gender": ["Male", "Female"],
        "SeniorCitizen": [0, 1],
        "Partner": ["Yes", "No"],
        "Dependents": ["No", "No"],
        "tenure": [1, 34],
        "PhoneService": ["Yes", "Yes"],
        "MultipleLines": ["No", "Yes"],
        "InternetService": ["DSL", "Fiber optic"],
        "OnlineSecurity": ["No", "Yes"],
        "OnlineBackup": ["Yes", "No"],
        "DeviceProtection": ["No", "Yes"],
        "TechSupport": ["No", "No"],
        "StreamingTV": ["No", "Yes"],
        "StreamingMovies": ["No", "No"],
        "Contract": ["Month-to-month", "One year"],
        "PaperlessBilling": ["Yes", "No"],
        "PaymentMethod": ["Electronic check", "Mailed check"],
        "MonthlyCharges": [29.85, 56.95],
        "TotalCharges": [29.85, 1889.5],
        "Churn": ["No", "No"],
        "churn_flag": [False, False]
    })
