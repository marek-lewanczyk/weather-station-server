# weather_app/utils/plotting.py

import matplotlib.pyplot as plt
import io
import base64

def generate_plot(data, fields=None, title=None):
    if not data or fields is None:
        return None

    plt.figure(figsize=(10, 5))

    # Tryb 1: domyślny – lista obiektów WeatherData + lista pól
    if isinstance(fields, list):
        timestamps = [record.timestamp.strftime("%Y-%m-%d %H:%M") for record in data]
        for field in fields:
            values = [getattr(record, field, None) for record in data]
            if any(v is not None for v in values):
                plt.plot(timestamps, values, label=field.capitalize())

    # Tryb 2: dane agregowane – data = lista X, fields = dict label: Y
    elif isinstance(fields, dict):
        x = data
        for label, values in fields.items():
            plt.plot(x, values, label=label)

    if title:
        plt.title(title)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()
