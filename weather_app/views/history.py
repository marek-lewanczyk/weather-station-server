# weather_app/views/history.py
from datetime import datetime, timedelta
from typing import List, Dict

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from weather_app.database import get_db
from weather_app.models import WeatherData
from weather_app.utils.plotting import generate_plot

router = APIRouter()
templates = Jinja2Templates(directory="weather_app/templates")


@router.get("/history", response_class=HTMLResponse)
async def history(request: Request, db: Session = Depends(get_db)):
    # ---------- 7-dniowa oś czasu (jak dotychczas) ----------
    since_7 = datetime.utcnow() - timedelta(days=7)
    history_7 = (
        db.query(WeatherData)
        .filter(WeatherData.timestamp >= since_7)
        .order_by(WeatherData.timestamp.asc())
        .all()
    )

    plot_temp_7 = generate_plot(history_7, ["temperature"])
    plot_pressure_7 = generate_plot(history_7, ["pressure"])
    plot_rain_7 = generate_plot(history_7, ["rain_mm"])
    plot_wind_7 = generate_plot(history_7, ["wind_kmph"])

    # ---------- Średnie dobowe z 30 dni ----------
    since_30 = datetime.utcnow() - timedelta(days=30)

    # grupowanie po dacie (bez czasu) + AVG
    daily_avgs: List[Dict] = (
        db.query(
            func.date(WeatherData.timestamp).label("day"),
            func.avg(WeatherData.temperature).label("avg_temp"),
            func.avg(WeatherData.pressure).label("avg_pressure"),
            func.avg(WeatherData.rain_mm).label("avg_rain"),
            func.avg(WeatherData.wind_kmph).label("avg_wind"),
        )
        .filter(WeatherData.timestamp >= since_30)
        .group_by("day")
        .order_by("day")
        .all()
    )

    # zamieniamy wyniki na listy dla generatora wykresów
    days = [str(row.day) for row in daily_avgs]
    avg_temp = [row.avg_temp for row in daily_avgs]
    avg_pressure = [row.avg_pressure for row in daily_avgs]
    avg_rain = [row.avg_rain for row in daily_avgs]
    avg_wind = [row.avg_wind for row in daily_avgs]

    plot_temp_avg = generate_plot(
        days,
        {"Średnia dobowa (°C)": avg_temp},
        title="Średnia dobowa temperatury – 30 dni",
    )
    plot_pressure_avg = generate_plot(
        days,
        {"Średnia dobowa (hPa)": avg_pressure},
        title="Średnia dobowa ciśnienia – 30 dni",
    )
    plot_rain_avg = generate_plot(
        days,
        {"Średnie opady (mm)": avg_rain},
        title="Średnie dobowe opady – 30 dni",
    )
    plot_wind_avg = generate_plot(
        days,
        {"Średnia prędkość (km/h)": avg_wind},
        title="Średnia dobowa prędkość wiatru – 30 dni",
    )

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "history": history_7,                    # tabela szczegółowa
            # 7-dniowe wykresy
            "plot_temp_7": plot_temp_7,
            "plot_pressure_7": plot_pressure_7,
            "plot_rain_7": plot_rain_7,
            "plot_wind_7": plot_wind_7,
            # 30-dniowe średnie dobowe
            "plot_temp_avg": plot_temp_avg,
            "plot_pressure_avg": plot_pressure_avg,
            "plot_rain_avg": plot_rain_avg,
            "plot_wind_avg": plot_wind_avg,
        },
    )
