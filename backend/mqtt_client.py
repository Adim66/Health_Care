import json
import paho.mqtt.client as mqtt
from health_records import save_health_record, analyze_record
BROKER = "localhost"
PORT = 1883
TOPIC = "#"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode().strip()
    if not payload_str:
        print(f"Empty message on {msg.topic}, skipping")
        return
    try:
        payload = json.loads(payload_str)
        print(f"Message received on {msg.topic}: {payload}")
        save_health_record(payload)
    except json.JSONDecodeError:
        print(f"Invalid JSON received on {msg.topic}: {payload_str}")


client = mqtt.Client("python_subscriber")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()
