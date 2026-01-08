import pandas as pd 
import datetime

def clean_transcation(raw_data):
    """Basic cleaning for the data science cycle."""
    raw_data['timestamp'] = dattime.datetime.now
    raw_data['amount'] = float(raw_data['amount'])
    return raw_data

def simulate_live_feed():
    """Simulates real-time data ingestion."""
    return {
        "user_id": "user_123",
        "merchant": "unknown_vendor",
        "amount": 5000.00,
        "ip": "192.168.1.1"
    }