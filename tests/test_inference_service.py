import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from src.inference_service import app, model


# Test 1: Health endpoint works
def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test 2: Prediction endpoint with mocked model
def test_predict_endpoint(monkeypatch):
    client = TestClient(app)

    # Mock model.predict_proba
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = [[0.3, 0.7]]  # 70% default probability

    # Patch the global model in inference_service
    monkeypatch.setattr("src.inference_service.model", mock_model)

    payload = {
        "customer_id": "CUST123",
        "txn_count": 10,
        "total_debit": -500.0,
        "total_credit": 2000.0,
        "avg_amount": 150.0,
        "kw_rent": 1,
        "kw_netflix": 0,
        "kw_tesco": 1,
        "kw_payroll": 0,
        "kw_bonus": 0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["customer_id"] == "CUST123"
    assert data["probability"] == 0.7
    assert data["prediction"] == 1  # because 0.7 >= 0.5
