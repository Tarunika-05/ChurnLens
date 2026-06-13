"""Tests for FastAPI endpoints."""
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "model_loaded" in data

def test_predict_single_invalid_data():
    """Test prediction with invalid schema returns 422."""
    response = client.post("/api/v1/predict", json={"gender": "Unknown"})
    assert response.status_code == 422
