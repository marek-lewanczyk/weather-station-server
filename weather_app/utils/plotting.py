# weather_app/utils/plotting.py

import matplotlib.pyplot as plt
import io
import base64

def generate_plot(data, fields=None):
    if not data or fields is None:
        return None

    timestamps = [record.timestamp.strftime("%Y-%m-%d %H:%M") for record in data]

    plt.figure(figsize=(10, 5))

    for field in fields:
        values = [getattr(record, field, None) for record in data]
        if any(v is not None for v in values):
            plt.plot(timestamps, values, label=field.capitalize())

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()
