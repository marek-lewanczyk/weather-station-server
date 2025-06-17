# weather_app/views/history.py

from datetime import datetime, timedelta
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from weather_app.database import get_db
from weather_app.models import WeatherData
from weather_app.utils.plotting import generate_plot

templates = Jinja2Templates(directory="weather_app/templates")

async def history(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    since = datetime.utcnow() - timedelta(days=7)
    history_data = (
        db.query(WeatherData)
        .filter(WeatherData.timestamp >= since)
        .order_by(WeatherData.timestamp.asc())
        .all()
    )

    if not history_data:
        return templates.TemplateResponse("history.html", {
            "request": request,
            "history": [],
            "plot_image": None
        })

    plot_image = generate_plot(history_data, fields=["temperature", "pressure"])

    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history_data,
        "plot_image": plot_image
    })
