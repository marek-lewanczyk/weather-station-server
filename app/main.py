from fastapi import FastAPI

from app.api.v1.router import api_router
from app.database import Base, engine
from app.views.dashboard import router as dashboard_router
from app.views.history import router as history_router



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather Station API",
    version="1.0.0"
)

app.include_router(api_router)
app.include_router(dashboard_router)
app.include_router(history_router)