import unittest
import base64
from datetime import datetime, timedelta
from server.weather_app.utils.plotting import generate_plot

class DummyWeatherData:
    def __init__(self, timestamp, temperature=None, humidity=None):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity

class TestGeneratePlot(unittest.TestCase):
    def test_empty_data_returns_none(self):
        result = generate_plot([], fields=["temperature"])
        self.assertIsNone(result)

    def test_none_fields_returns_none(self):
        data = [DummyWeatherData(datetime.now(), 20)]
        result = generate_plot(data, fields=None)
        self.assertIsNone(result)

    def test_generate_plot_from_objects(self):
        now = datetime.now()
        data = [
            DummyWeatherData(now - timedelta(minutes=i), temperature=20 + i, humidity=50 + i)
            for i in range(5)
        ]
        result = generate_plot(data, fields=["temperature", "humidity"], title="Test Plot")
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith(base64.b64encode(b'\x89PNG').decode()[:5]))  # Starts like PNG

    def test_generate_plot_from_dict(self):
        x = ['00:00', '01:00', '02:00']
        y_data = {
            'Temperature': [20, 21, 22],
            'Humidity': [50, 52, 55]
        }
        result = generate_plot(x, fields=y_data, title="Test Dict Plot")
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith(base64.b64encode(b'\x89PNG').decode()[:5]))

if __name__ == "__main__":
    unittest.main()