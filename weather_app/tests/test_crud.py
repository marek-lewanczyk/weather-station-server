# weather_app/tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from weather_app import models, schemas, crud
from weather_app.database import Base

# Tworzymy bazę w pamięci (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture do sesji DB
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# Test funkcji create_weather_data
def test_create_weather_data(db):
    input_data = schemas.WeatherDataIn(
        temperature=22.5,
        humidity=55.0,
        pressure=1013.25,
        rain_mm=0.0,
        wind_kmph=15.0
    )

    result = crud.create_weather_data(db, input_data)

    assert result.id is not None
    assert result.temperature == input_data.temperature
    assert result.humidity == input_data.humidity
    assert result.pressure == input_data.pressure
    assert result.rain_mm == input_data.rain_mm
    assert result.wind_kmph == input_data.wind_kmph
    assert result.timestamp is not None