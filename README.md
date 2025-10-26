# PoC — Real-Time Health System (Proof-of-Concept)

**Overview.**  
This is a proof-of-concept demonstrating real-time health data ingestion. A smartwatch simulates measurements and relays them through a mobile application to an asynchronous backend architecture. The goal is to showcase a scalable pub/sub pipeline agnostic to protocols.

---

## Architecture (Summary)
- **Simulated Client:** Smartwatch → generates time series \( s(t) \).  
- **Mobile App:** Relay, converts \( s(t) \) into messages \( m(t) \).  
- **Backend:** 3 FastAPI microservices (\( B_1, B_2, B_3 \)).  
- **Broker:** Mosquitto (MQTT) for asynchronous distribution.

Mathematically:  
Let \( s(t) \) be the measurement at time \( t \). Data flow:
\[
s(t) \xrightarrow{\text{Mobile}} m(t) \xrightarrow{\text{HTTP/WebSocket/MQTT}} B_i \xrightarrow{\text{publish}} \text{Broker(topic)} \xrightarrow{\text{subscribe}} B_j
\]

---

## Components & Roles
- **Mosquitto (MQTT):** pub/sub broker with structured topics.  
- **FastAPI (Python):** three services exposing HTTP and WebSocket endpoints. They publish/subscribe to the broker.  
- **Mobile App (simulated):** sends data via HTTP, WebSocket, or MQTT.  
- **Smartwatch (simulated):** produces JSON payloads (heart rate, SpO2, acceleration, timestamp).

---


## MQTT Topics (Convention)
- `health/{device_id}/telemetry` — real-time raw data.  
- `health/{device_id}/alerts` — clinical alerts.  
- `health/aggregate` — aggregated metrics.

---

## Message Format (JSON Example)
```json
{
  "device_id": "watch-001",
  "timestamp": "2025-10-26T12:34:56Z",
  "metrics": {
    "hr": 78,
    "spo2": 97,
    "accel": [0.01, -0.02, 0.98]
  },
  "meta": {
    "protocol": "mqtt",
    "seq": 1234
  }
}
