
# import urequests
# import ujson
# import network
# import time
# from machine import Pin
# import dht

# ssid = "NAZWA_TWOJEJ_SIECI"
# password = "HASLO_TWOJEJ_SIECI"

# def connect_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(ssid, password)
#     while not wlan.isconnected():
#         print("Łączenie z WiFi...")
#         time.sleep(1)
#     print("Połączono:", wlan.ifconfig())

# def send_data():
#     sensor = dht.DHT22(Pin(4))  # GPIO4
#     while True:
#         sensor.measure()
#         temperature = sensor.temperature()
#         humidity = sensor.humidity()

#         data = {
#             "temperature": temperature,
#             "humidity": humidity,
#             "pressure": 1013,
#             "gas": 9000,
#             "rain_mm": 0.0,
#             "rain_mm_total": 0.0,
#             "wind_kmph": 5.0,
#             "wind_deg": 180
#         }

#         try:
#             response = urequests.post(
#                 "http://192.168.1.100:8000/data",  # <- IP Twojego komputera
#                 headers={"Content-Type": "application/json"},
#                 data=ujson.dumps(data)
#             )
#             print("Wysłano:", response.status_code)
#             response.close()
#         except Exception as e:
#             print("Błąd:", e)

#         time.sleep(10)

# # Użycie:
# # connect_wifi()
# # send_data()
