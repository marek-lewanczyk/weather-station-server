import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from weather_app.main import app
from weather_app.database import get_db, Base
from weather_app.models import WeatherData

# 🔧 KLUCZOWA zmiana tutaj
SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False, "uri": True}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ❗ Musi być przed utworzeniem klienta
Base.metadata.create_all(bind=engine)

# 🔁 Nadpisanie zależności FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_dashboard_view():
    db = TestingSessionLocal()
    db.add(WeatherData(
        temperature=20.5,
        humidity=60.0,
        pressure=1013.0,
        wind_kmph=15.0,
        rain_mm=0.2
    ))
    db.commit()
    db.close()

    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "temperature" in response.text or "20.5" in response.text
