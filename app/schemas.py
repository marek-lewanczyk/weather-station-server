# app/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherDataIn(BaseModel):
    temperature: float
    humidity: float
    pressure: Optional[float] = None
    wind_kmph: Optional[float] = None
    wind_deg: Optional[float] = None
    rain_mm: Optional[float] = None
    rain_mm_total: Optional[float] = None
    gas: Optional[float] = None

class WeatherDataOut(WeatherDataIn):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True