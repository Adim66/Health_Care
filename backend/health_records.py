# health_records.py
import datetime

# Stockage en mémoire (tu peux remplacer par une DB comme SQLite, MongoDB, PostgreSQL)
records = []

def save_health_record(data):
    """
    Sauvegarde un enregistrement de santé reçu du simulateur ou du broker.
    Ajoute un timestamp.
    """
    record = data.copy()
    record["timestamp"] = datetime.datetime.now().isoformat()
    records.append(record)
    print(f"Record saved: {record}")

def get_latest_records(limit=10):
    """
    Retourne les derniers enregistrements.
    """
    return records[-limit:]

def analyze_record(data):
    """
    Exemple d'analyse simple : détecte des anomalies.
    """
    alerts = []
    if data.get("heart_rate", 0) > 120:
        alerts.append("High heart rate")
    if data.get("temperature", 0) > 38:
        alerts.append("High temperature")
    if data.get("spo2", 100) < 90:
        alerts.append("Low oxygen saturation")
    return {"alerts": alerts, "status": "OK" if not alerts else "ALERT"}
