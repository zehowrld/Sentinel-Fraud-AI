import requests
import pandas as pd 
from src.utils import get_env_keys, logger



def fetch_live_market_data():
    """Fetches live crypto market data as a proxy for financial transactions."""
    keys = get_env_keys()
    if not keys.get("COINGECKO_KEY"):
        logger.error("❌ Ingestion failed: COINGECKO_KEY is missing from environment.")
        return None
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }
    headers = {
        "x-cg-demo-api-key": keys["COINGECKO_KEY"],
        "accept": "application/json"               
    }

    try: 
        logger.info("📡 Ingestor: Requesting 250 raw transactions from CoinGecko...")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Convert to DataFrame (Cleaning/Normalization step)
        df = pd.json_normalize(data)
        logger.info(f"✅ Successfully ingested {len(df)} live transactions.")
        return df 
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        return None

if __name__ == "__main__":
    # Test the ingestion
    data = fetch_live_market_data()
    if data is not None:
        print(f"Sample Data (First 5 of {len(data)}):")
        print(data[['id', 'symbol', 'current_price']].head())