# test_weather_routes.py
import pytest
from fastapi.testclient import TestClient
from weather_app.main import app

client = TestClient(app)

def test_post_valid_weather():
    sample = {
        "temperature": 21.1,
        "humidity": 50.0,
        "pressure": 1012.3,
        "wind_kmph": 12.0,
        "rain_mm": 0.0
    }

    response = client.post("/weather", json=sample)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["temperature"] == sample["temperature"]
