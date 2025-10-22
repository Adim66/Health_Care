import streamlit as st
import requests
import asyncio
import websockets
import json
import time
import matplotlib.pyplot as plt

# ===================== CONFIG =====================
STORAGE_URL = "http://127.0.0.1:8003/api/data"
VISUAL_WS_URL = "ws://127.0.0.1:8005/ws"

st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide")

# ===================== LAYOUT =====================
st.title("🩺 Real-Time Health Dashboard")

# Création d'une grille avec deux colonnes
col1, col2 = st.columns([1, 1])

# ===================== HISTORIQUE =====================
with col1:
    st.subheader("📈 Historical Metrics Viewer")
    show_history = st.button("Afficher l'historique")

    if show_history:
        st.info("Fetching historical data...")
        try:
            resp = requests.get(STORAGE_URL)
            if resp.status_code == 200:
                data = resp.json()
                if not data:
                    st.warning("Aucune donnée disponible.")
                else:
                    # Afficher chaque métrique dans une courbe
                    timestamps = [d.get("ts", i) for i, d in enumerate(data)]
                    heart_rates = [d.get("heart_rate", 0) for d in data]

                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.plot(timestamps, heart_rates, marker="o", label="Heart Rate")
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Heart Rate (bpm)")
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)
            else:
                st.error(f"Erreur HTTP: {resp.status_code}")
        except Exception as e:
            st.error(f"Erreur de connexion: {e}")

# ===================== TEMPS REEL =====================
with col2:
    st.subheader("⚡ Real-Time Health Indicator")
    placeholder = st.empty()

async def realtime_view():
    async with websockets.connect(VISUAL_WS_URL) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            
            # Extraction de latest_data
            f_val = data.get("1", 0)   # valeur calculée par service 2
            a_val = data.get("2", 0)   # 0 ou 1

            # Définition couleur et rayon
            color = "green" if a_val == 1 else "red"
            radius = 0.3 + 0.4 * f_val  # rayon proportionnel à la valeur calculée

            # Création du cercle animé
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.axis("off")
            circle = plt.Circle((0, 0), radius=radius, color=color, alpha=0.6)
            ax.add_artist(circle)
            ax.text(0, 0, f"f={f_val:.3f}\nStatus={'Normal' if a_val==1 else 'Alerte'}", 
                    fontsize=12, ha="center", va="center")
            placeholder.pyplot(fig)

            # Pause pour animation
            time.sleep(1.5)

# Lancer l’écoute WebSocket
st.info("Connexion temps réel en cours...")
asyncio.run(realtime_view())
