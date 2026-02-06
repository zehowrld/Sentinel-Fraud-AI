import os
import requests
from dotenv import load_dotenv
from openai import OpenAI 

# Load the keys we saved in .env
load_dotenv()

def test_connections():
    print("🚀 Starting API Connectivity Test...")

    # 1. Test CoinGecko
    cg_url = "https://api.coingecko.com/api/v3/ping"
    cg_res = requests.get(cg_url)
    print(f"✅ CoinGecko: {'Online' if cg_res.status_code == 200 else 'Failed'}")

    # 2. Test IPQualityScore
    ip_key = os.get("IP_QUALITY_KEY")
    ip_url = f"https://www.ipqualityscore.com/api/json/ip/{ip_key}/8.8.8.8"
    ip_res = requests.get(ip_url)
    print(f"✅ IPQualityScore: {'Online' if ip_res.status_code == 200 else 'Failed'}")

    # 3. Test OpenAI
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("✅ OpenAI: Key Valid")
    except:
        print("❌ OpenAI: Authentication Failed")

if __name__ == "__main__":
    test_connections()