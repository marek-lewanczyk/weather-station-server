from fastapi.testclient import TestClient
from weather_app.main import app

client = TestClient(app)

def test_post_weather_data():
    payload = {
        "temperature": 23.5,
        "pressure": 1012.3,
        "humidity": 60.5,
        "wind_kmph": 12.3,
        "rain_mm": 1.2
    }

    response = client.post("/weather", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["temperature"] == payload["temperature"]
    assert data["pressure"] == payload["pressure"]
    assert data["humidity"] == payload["humidity"]
    assert data["wind_kmph"] == payload["wind_kmph"]
    assert data["rain_mm"] == payload["rain_mm"]
    assert "timestamp" in data