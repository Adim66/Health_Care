# health_service.py
from fastapi import FastAPI
import paho.mqtt.client as mqtt
import threading
import json
import math
import time

app = FastAPI(title="Health Calculation Service")

BROKER = "localhost"
PORT = 1883

def compute_health(heart_rate: float, spo2: float, temperature: float) -> float:
    """
    Calcule un score de santé global entre 0 et 1.
    1 = état optimal, 0 = anomalie sévère
    """
    # Normalisation des écarts par rapport à des valeurs "idéales"
    hr_score = math.exp(-abs(heart_rate - 75) / 15)       # idéal ≈ 75 bpm
    spo2_score = math.exp(-abs(spo2 - 98) / 2)            # idéal ≈ 98%
    temp_score = math.exp(-abs(temperature - 37) / 0.5)   # idéal ≈ 37°C

    # Moyenne pondérée (on peut ajuster les poids)
    health = (0.4 * hr_score) + (0.4 * spo2_score) + (0.2 * temp_score)

    return round(health, 3)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    hr = data.get("heart_rate", 70)
    spo2 = data.get("spo2", 98)
    temperature = data.get("temperature", 37.0)
    health = compute_health(hr, spo2, temperature)
    result = {"id": data.get("id"), "health": health, "ts": time.time()}
    print("Computed at service 2 ", result)
    client.publish("health/score", json.dumps(health))

def start_mqtt():
    client = mqtt.Client("health_service")
    client.connect(BROKER, PORT)
    client.subscribe("health/watch1/metrics")
    client.on_message = on_message
    client.loop_start()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_mqtt, daemon=True).start()

@app.get("/status")
def status():
    return {"status": "Health calculator running"}
