# weather_app/views/history.py

from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WeatherData
from app.utils.plotting import generate_plot

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/history", response_class=HTMLResponse)
async def history(request: Request, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=7)
    history_data = (
        db.query(WeatherData)
        .filter(WeatherData.timestamp >= since)
        .order_by(WeatherData.timestamp.asc())
        .all()
    )

    # ------- Wykresy (bez trzeciego parametru) -------Add commentMore actions
    plot_temp_pressure = generate_plot(
        history_data,
        ["temperature", "pressure"]
    )

    plot_rain = generate_plot(
        history_data,
        ["rain_mm"]
    )

    plot_wind = generate_plot(
        history_data,
        ["wind_kmph"]
    )

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "history": history_data,
            "plot_temp_pressure": plot_temp_pressure,
            "plot_rain": plot_rain,
            "plot_wind": plot_wind,
        },
    )
