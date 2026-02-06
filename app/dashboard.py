import streamlit as st 
from src.ingestor import fetch_live_market_data

st.set_page_config(page_title="Sentinel Fraud 2026", layout="wide")

st.title("🛡️ Sentinel-Graph AI")
st.write("Real-time Graph-Based Detection")

if st.button('Fetch Live Data'):
    with st.spinner('Ingesting...'):
        df = fetch_live_market_data()
        if df is not None:
            st.success("Data Ingested")
            st.dataframe(df[['name', 'current_price', 'price_change_percentage_24h']])
        else:
            st.error("Check your API keys.")
