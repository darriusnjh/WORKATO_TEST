import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Calculator API" in response.json()["message"]


def test_addition():
    response = client.post("/calculate", json={
        "operation": "+",
        "num1": 10,
        "num2": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 15
    assert data["operation"] == "+"


def test_subtraction():
    response = client.post("/calculate", json={
        "operation": "-",
        "num1": 10,
        "num2": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5


def test_multiplication():
    response = client.post("/calculate", json={
        "operation": "*",
        "num1": 10,
        "num2": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 50


def test_division():
    response = client.post("/calculate", json={
        "operation": "/",
        "num1": 10,
        "num2": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 2


def test_division_by_zero():
    response = client.post("/calculate", json={
        "operation": "/",
        "num1": 10,
        "num2": 0
    })
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["detail"]


def test_invalid_operation():
    response = client.post("/calculate", json={
        "operation": "%",
        "num1": 10,
        "num2": 5
    })
    assert response.status_code == 422  # Validation error for invalid literal


def test_current_time_default_utc():
    response = client.get("/current-time")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    assert data["timezone"] == "UTC"
    assert "timestamp" in data
    assert isinstance(data["timestamp"], float)


def test_current_time_with_timezone():
    response = client.get("/current-time?timezone=Asia/Singapore")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    assert data["timezone"] == "Asia/Singapore"
    assert "timestamp" in data


def test_current_time_invalid_timezone():
    response = client.get("/current-time?timezone=Invalid/Timezone")
    assert response.status_code == 400
    assert "Invalid timezone" in response.json()["detail"]
