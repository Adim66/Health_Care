# backend/main.py
from fastapi import FastAPI
from health_records import get_latest_records
import mqtt_client  # Importe le client MQTT déjà lancé en arrière-plan

app = FastAPI()

# Endpoint pour récupérer les derniers enregistrements
@app.get("/api/data")
def get_health_data(limit: int = 10):
    """
    Retourne les derniers enregistrements de santé
    """
    return get_latest_records(limit)
