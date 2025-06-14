# app/api/v1/endpoints/weather.py

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.WeatherDataOut, status_code=status.HTTP_201_CREATED)
def post_weather(data: schemas.WeatherDataIn, db: Session = Depends(get_db)):
    return crud.create_weather_data(db, data)

@router.get("/", response_model=List[schemas.WeatherDataOut])
def get_all_weather(db: Session = Depends(get_db)):
    return db.query(models.WeatherData).order_by(models.WeatherData.timestamp.desc()).all()