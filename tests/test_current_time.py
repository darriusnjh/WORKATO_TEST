import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)


def test_get_current_time_default_utc():
    response = client.get("/current-time")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    assert data["timezone"] == "UTC"
    assert "timestamp" in data
    assert isinstance(data["timestamp"], float)


def test_get_current_time_specific_timezone():
    response = client.get("/current-time?timezone=Asia/Singapore")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    assert data["timezone"] == "Asia/Singapore"
    assert "timestamp" in data


def test_get_current_time_new_york():
    response = client.get("/current-time?timezone=America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"
    assert "EDT" in data["current_time"] or "EST" in data["current_time"]


def test_get_current_time_london():
    response = client.get("/current-time?timezone=Europe/London")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "Europe/London"


def test_get_current_time_invalid_timezone():
    response = client.get("/current-time?timezone=Invalid/Timezone")
    assert response.status_code == 400
    assert "Invalid timezone" in response.json()["detail"]


def test_current_time_format():
    response = client.get("/current-time")
    assert response.status_code == 200
    data = response.json()
    current_time_str = data["current_time"]
    
    # Check format is "YYYY-MM-DD HH:MM:SS TZ"
    assert len(current_time_str.split()) >= 3
    date_part = current_time_str.split()[0]
    assert len(date_part.split("-")) == 3  # Year-Month-Day

