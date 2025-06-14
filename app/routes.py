# app/routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/weather",
    response_model=schemas.WeatherDataOut,
    status_code=status.HTTP_201_CREATED
)
def post_weather_data(data: schemas.WeatherDataIn, db: Session = Depends(get_db)):
    return crud.create_weather_data(db=db, data=data)