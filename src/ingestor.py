import requests
import pandas as pd 
from src.utils import get_env_keys, logger

keys = get_env_keys()

def fetch_live_market_data():
    """Fetches live crypto market data as a proxy for financial transactions."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    headers = {"x-cg-demo-api-key": keys["COINGECKO_KEY"]}

    try: 
        response =requests.get(url, params=params, headers=headers)
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
    print(data.head())