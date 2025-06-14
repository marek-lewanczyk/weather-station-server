# app/main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.api.v1.router import api_router  # <- zmienione z routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather Station API",
    version="1.0.0"
)

app.include_router(api_router)