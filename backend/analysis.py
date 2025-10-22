def analyze(data):
    alerts = []
    if data["heart_rate"] > 100:
        alerts.append("High heart rate")
    if data["spo2"] < 95:
        alerts.append("Low oxygen level")
    if data["temperature"] > 37.5:
        alerts.append("Fever detected")
    return {"alerts": alerts, "status": "OK" if not alerts else "ALERT"}
