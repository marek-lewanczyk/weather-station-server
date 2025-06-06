import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime
import os

class WeatherPlotter:
    def __init__(self, max_points=100):
        self.timestamps = deque(maxlen=max_points)
        self.temperature = deque(maxlen=max_points)
        self.humidity = deque(maxlen=max_points)
        self.pressure = deque(maxlen=max_points)
        self.gas = deque(maxlen=max_points)
        self.rain_mm = deque(maxlen=max_points)
        self.rain_total = deque(maxlen=max_points)
        self.wind_kmph = deque(maxlen=max_points)

        os.makedirs("images", exist_ok=True)

    def add_data(self, data):
        now = datetime.now().strftime('%H:%M:%S')
        self.timestamps.append(now)
        self.temperature.append(data.get('temperature'))
        self.humidity.append(data.get('humidity'))
        self.pressure.append(data.get('pressure'))
        self.gas.append(data.get('gas'))
        self.rain_mm.append(data.get('rain_mm'))
        self.rain_total.append(data.get('rain_mm_total'))
        self.wind_kmph.append(data.get('wind_kmph'))

    def save_all_plots(self):
        self._plot_to_file(self.temperature, self.humidity, "Temperatura i wilgotność", "images/temp_humidity.png",
                           ["Temperatura [°C]", "Wilgotność [%]"])
        self._plot_to_file(self.wind_kmph, None, "Prędkość wiatru", "images/wind.png", ["Wiatr [km/h]"])
        self._plot_to_file(self.rain_total, self.rain_mm, "Opady deszczu", "images/rain.png",
                           ["Opady (1h) [mm]", "Opady (odczyt) [mm]"])
        self._plot_to_file(self.gas, None, "Gaz (jakość powietrza)", "images/gas.png", ["Gaz [Ω]"])
        self._plot_to_file(self.pressure, None, "Ciśnienie", "images/pressure.png", ["Ciśnienie [hPa]"])


    def _plot_to_file(self, series1, series2, title, filename, labels):
        if not any(series1):
            return
        plt.figure(figsize=(10, 5))
        plt.plot(self.timestamps, series1, marker='o', label=labels[0])
        if series2 and any(series2):
            plt.plot(self.timestamps, series2, marker='o', label=labels[1])
        plt.title(title)
        plt.xlabel("Czas")
        plt.ylabel("Wartość")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        plt.close()
