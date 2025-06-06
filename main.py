from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from weather_plotter import WeatherPlotter
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

plotter = WeatherPlotter()

# Serwowanie folderu z obrazami
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    print("Odebrano dane:", data)
    plotter.add_data(data)
    plotter.save_all_plots()

    return {"status": "ok"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "rand": random.randint(0, 99999)
    })
