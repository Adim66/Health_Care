import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "health/watch1/metrics"

client = mqtt.Client("watch_simulator")
client.connect(BROKER, PORT, 60)

while True:
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "heart_rate": random.randint(60, 120),
        "spo2": random.randint(90, 100),
        "temperature": round(random.uniform(36.0, 38.0), 1)
    }
    client.publish(TOPIC, json.dumps(data))
    print(f"Published: {data}")
    time.sleep(3)
