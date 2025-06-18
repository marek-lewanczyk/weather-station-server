from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from weather_app.database import get_db
from weather_app.models import WeatherData
from weather_app.utils.plotting import generate_plot

router = APIRouter()
templates = Jinja2Templates(directory="weather_app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    latest = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).first()
    history = (
        db.query(WeatherData)
        .order_by(WeatherData.timestamp.desc())
        .limit(10)
        .all()
    )[::-1]  # chronologicznie

    # Wykresy na zakładkach
    plot_temp = generate_plot(history, ["temperature"])
    plot_pressure = generate_plot(history, ["pressure"])
    rain_plot           = generate_plot(history, ["rain_mm"])
    wind_plot           = generate_plot(history, ["wind_kmph"])

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "latest": latest,
        "plot_temp": plot_temp,
        "plot_pressure": plot_pressure,
        "plot_rain": rain_plot,
        "plot_wind": wind_plot,
    })

