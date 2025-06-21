#!/bin/bash
source .venv/bin/activate
uvicorn weather_app.main:app --host 0.0.0.0 --port 8000 --reload