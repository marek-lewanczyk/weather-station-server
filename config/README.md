# 🌦️ Stacja pogodowa – uruchomienie z ESP32

Po podłączeniu urządzenia (ESP32) i skonfigurowaniu połączenia Wi-Fi, wykonaj poniższe kroki, aby rozpocząć przesyłanie danych do aplikacji:

## ✅ Krok 1: Uruchom backend FastAPI

1. Przejdź do katalogu `server/`.
2. Upewnij się, że środowisko wirtualne jest aktywne (`.venv`).
3. Uruchom serwer FastAPI:

```bash
uvicorn main:app --reload --port 8000
Wgraj wcześniej przygotowany kod MicroPython na ESP32 (np. przez Thonny).

Upewnij się, że:

dane Wi-Fi (SSID i hasło) są poprawnie wpisane,

adres IP w urequests.post(...) wskazuje na Twój komputer (np. http://192.168.1.X:8000/data).

Po uruchomieniu ESP32:

urządzenie połączy się z siecią Wi-Fi,

co 10 sekund wyśle dane do endpointa /data.

