from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_addition():
    resp = client.post("/calculate", json={"a": 2, "b": 3, "operator": "+"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_subtraction():
    resp = client.post("/calculate", json={"a": 5, "b": 3, "operator": "-"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 2


def test_multiplication():
    resp = client.post("/calculate", json={"a": 4, "b": 6, "operator": "*"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 24


def test_division():
    resp = client.post("/calculate", json={"a": 8, "b": 2, "operator": "/"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 4


def test_divide_by_zero():
    resp = client.post("/calculate", json={"a": 1, "b": 0, "operator": "/"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Division by zero is not allowed"


def test_invalid_operator_validation():
    resp = client.post("/calculate", json={"a": 1, "b": 2, "operator": "%"})
    assert resp.status_code == 422


