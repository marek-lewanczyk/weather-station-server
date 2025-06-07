from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from weather_plotter import WeatherPlotter
from pathlib import Path
from datetime import datetime
from database import SessionLocal, init_db
from models import WeatherData
import random

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

plotter = WeatherPlotter()

# Serwowanie folderu z obrazami
app.mount("/images", StaticFiles(directory="images"), name="images")

# Funkcja do pobierania sesji DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/data")
async def receive_data(request: Request, db=Depends(get_db)):
    data = await request.json()
    print("Odebrano dane:", data)

    # Zapis do wykresów
    plotter.add_data(data)
    plotter.plot()

    # Zapis do bazy danych
    entry = WeatherData(
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        pressure=data.get("pressure"),
        gas=data.get("gas"),
        rain_mm=data.get("rain_mm"),
        rain_mm_total=data.get("rain_mm_total"),
        wind_kmph=data.get("wind_kmph"),
        wind_deg=data.get("wind_deg"),
    )
    db.add(entry)
    db.commit()

    return {"status": "ok"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "rand": random.randint(0, 99999)
    })

# Inicjalizacja bazy danych przy starcie serwera
@app.on_event("startup")
def startup():
    init_db()

@app.get("/data/history")
async def get_history(db: Session = Depends(get_db)):
    results = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(100).all()
    data = [
        {
            "timestamp": row.timestamp,
            "temperature": row.temperature,
            "humidity": row.humidity,
            "pressure": row.pressure,
            "gas": row.gas,
            "rain_mm": row.rain_mm,
            "rain_mm_total": row.rain_mm_total,
            "wind_kmph": row.wind_kmph,
            "wind_deg": row.wind_deg
        }
        for row in results
    ]
    return JSONResponse(content=data)
# Endpoint zwracający dane w JSON do JS
@app.get("/data/history/json")
async def get_history_json(db: Session = Depends(get_db)):
    results = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(100).all()
    data = [
        {
            "timestamp": row.timestamp.isoformat(),
            "temperature": row.temperature,
            "humidity": row.humidity,
            "pressure": row.pressure,
            "gas": row.gas,
            "rain_mm": row.rain_mm,
            "rain_mm_total": row.rain_mm_total,
            "wind_kmph": row.wind_kmph,
            "wind_deg": row.wind_deg
        }
        for row in results
    ]
    return JSONResponse(content=data)

# Endpoint HTML z widokiem historii
@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})
@app.on_event("startup")
def startup():
    init_db()
    # Dodanie przykładowego wpisu, jeśli tabela pusta
    db: Session = SessionLocal()
    if db.query(WeatherData).count() == 0:
        sample = WeatherData(
            timestamp=datetime.utcnow(),
            temperature=21.0,
            humidity=60.0,
            pressure=1010,
            gas=8900,
            rain_mm=0.3,
            rain_mm_total=1.5,
            wind_kmph=8.0,
            wind_deg=150
        )
        db.add(sample)
        db.commit()
        print("✅ Dodano przykładowy wpis testowy do bazy")
    db.close()