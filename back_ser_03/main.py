# visual_service.py
import asyncio
from fastapi import FastAPI, WebSocket
import paho.mqtt.client as mqtt
import threading
import json

app = FastAPI(title="Visualization Service")

def binary_classifier(x: float, threshold: float = 0.5) -> int:
    """
    Classifie un nombre réel en 0 ou 1 selon un seuil.
    x >= threshold -> 1
    x < threshold  -> 0
    """
    return 1 if x >= threshold else 0
latest_data = {"1": 0, "2":0 }

def on_message(client, userdata, msg):
    global latest_data
    data = json.loads(msg.payload.decode())
    
    
    latest_data["1"]= data
    b=data+0.19
    a= binary_classifier(b)
    latest_data["2"]= a
    print("Visual:", latest_data)

def start_mqtt():
    client = mqtt.Client("visual_service")
    client.connect("localhost", 1883)
    client.subscribe("health/score")
    client.on_message = on_message
    client.loop_start()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_mqtt, daemon=True).start()

@app.get("/latest")
def get_latest():
    return latest_data or {"message": "No data yet"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if latest_data:
            await websocket.send_json(latest_data)
        await asyncio.sleep(2)
