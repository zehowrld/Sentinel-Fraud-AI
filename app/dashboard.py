import streamlit as st 
import pandas as pd 

st.set_page_config(page_title="Sentinel Fraud 2026", layout="wide")
st.title("🛡️ Sentinel-Graph AI: Real-Time Fraud Monitor")

st.sidebar.header("System Status")
st.sidebar.success("GNN Model: Active")
st.sidebar.info("Agentic Layer: Listening")

# Placeholder for real-time table
df = pd.DataFrame([
    {"Time": "21:05", "User": "0x45f", "Amount": "$12,000", "Risk": "92%", "Status": "Investigating"}
])
st.table(df)

st.write("### Graph Network Visualization")
st.info("Interactive Graph Loading...")