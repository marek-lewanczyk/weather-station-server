from fastapi import FastAPI

from weather_app.api.v1.router import api_router
from weather_app.database import Base, engine
from weather_app.views.dashboard import router as dashboard_router
from weather_app.views.history import router as history_router
from weather_app.routes import router as weather_router


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Weather Station API",
    version="0.0.1"
)
app.include_router(api_router)
app.include_router(dashboard_router)
app.include_router(history_router)
app.include_router(weather_router)