# weather_app/api/v1/endpoints/weather.py

from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------
#  POST /weather  – zapis nowego pomiaru (z ESP32)
# ------------------------------------------------

@router.post(
    "/", response_model=schemas.WeatherDataOut, status_code=status.HTTP_201_CREATED
)
def post_weather(
    data: schemas.WeatherDataIn, db: Session = Depends(get_db)
):
    """Zapisuje nowy pomiar do bazy."""
    return crud.create_weather_data(db, data)

# -----------------------------------------------
#  GET /weather  – wszystkie pomiary (DESC)
# -----------------------------------------------

@router.get("/", response_model=List[schemas.WeatherDataOut])
def get_all_weather(db: Session = Depends(get_db)):
    return (
        db.query(models.WeatherData)
        .order_by(models.WeatherData.timestamp.desc())
        .all()
    )

# -------------------------------------------------
#  GET /weather/latest  – ostatni zapisany pomiar
# -------------------------------------------------

@router.get("/latest", response_model=schemas.WeatherDataOut)
def get_latest_weather(db: Session = Depends(get_db)):
    latest = (
        db.query(models.WeatherData)
        .order_by(models.WeatherData.timestamp.desc())
        .first()
    )
    if not latest:
        raise HTTPException(status_code=404, detail="No data yet")
    return latest

# --------------------------------------------------------------------
#  GET /weather/history?days=N  – pomiary z ostatnich N dni (default=7)
# --------------------------------------------------------------------

@router.get("/history", response_model=List[schemas.WeatherDataOut])
def get_weather_history(
    days: int = Query(7, ge=1, le=365), db: Session = Depends(get_db)
):
    """Zwraca pomiary z ostatnich *days* dni w kolejności rosnącej po czasie."""
    since = datetime.utcnow() - timedelta(days=days)
    history = (
        db.query(models.WeatherData)
        .filter(models.WeatherData.timestamp >= since)
        .order_by(models.WeatherData.timestamp.asc())
        .all()
    )
    return history
