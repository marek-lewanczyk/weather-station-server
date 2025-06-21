from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from weather_app.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=True)
    wind_kmph = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    rain_mm = Column(Float, nullable=True)
    rain_mm_total = Column(Float, nullable=True)
    gas = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)