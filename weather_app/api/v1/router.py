# weather_app/api/v1/router.py

from fastapi import APIRouter
from weather_app.api.v1.endpoints import weather

api_router = APIRouter()

# Dołączamy endpointy z weather.py
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])