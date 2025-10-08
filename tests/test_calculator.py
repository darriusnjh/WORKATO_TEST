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

