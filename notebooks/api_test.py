import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load the keys we saved in .env
load_dotenv()

def test_connections():
    print("🚀 Starting API Connectivity Test...")
    print("-" * 40)


    # 1. Test CoinGecko
    try:
        cg_url = "https://api.coingecko.com/api/v3/ping"
        cg_res = requests.get(cg_url, timeout=5)
        status = "✅ ONLINE" if cg_res.status_code == 200 else "❌ OFFLINE"
        print(f"CoinGecko Market API: {status}")
    except Exception as e:
        print(f"CoinGecko Market API: ❌ FAILED - {e}")

    # 2. Test IPQualityScore
    ip_key = os.getenv("IP_QUALITY_KEY")
    if not ip_key:
        print("IPQualityScore API: ⚠️ KEY MISSING IN .ENV")
    else:
        try:
            # We check the 'success' field in the JSON response
            ip_url = f"https://www.ipqualityscore.com/api/json/ip/{ip_key}/8.8.8.8"
            ip_res = requests.get(ip_url, timeout=5).json()
            if ip_res.get('success'):
                print("IPQualityScore API: ✅ KEY VALID & ONLINE")
            else:
                print(f"IPQualityScore API: ❌ INVALID KEY - {ip_res.get('message')}")
        except Exception as e:
            print(f"IPQualityScore API: ❌ FAILED - {e}")

    # 3. Test Gemini
    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        print("Gemini AI Engine: ⚠️ KEY MISSING IN .ENV")
    else:
        try:
            genai.configure(api_key=google_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # A tiny prompt to ensure the model actually responds
            response = model.generate_content("ping")
            if response.text:
                print("Gemini AI Engine: ✅ KEY VALID & RESPONDING")
        except Exception as e:
            print(f"Gemini AI Engine: ❌ FAILED - {e}")

    print("-" * 40)
    print("🏁 Connectivity Test Finished.")

if __name__ == "__main__":
    test_connections()