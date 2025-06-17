# weather_app/crud.py

from sqlalchemy.orm import Session
from weather_app import models, schemas

def create_weather_data(db: Session, data: schemas.WeatherDataIn) -> models.WeatherData:
    weather_entry = models.WeatherData(**data.dict())
    db.add(weather_entry)
    db.commit()
    db.refresh(weather_entry)
    return weather_entry