import streamlit as st
import requests

st.title("Health Monitoring Dashboard")

resp = requests.get("http://127.0.0.1:8000/health")
st.write("Backend Status:", resp.json())

st.subheader("Dernières alertes (backend console)")
st.info("Ouvre la console du backend pour voir les analyses en temps réel.")
