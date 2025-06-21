from fastapi.testclient import TestClient
from weather_app.main import app

def test_get_weather():
    client = TestClient(app)
    response = client.get("/weather")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
