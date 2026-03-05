import os 
import logging
from dotenv import load_dotenv

# Initialize logging to see what's happening in terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_env_keys():
    """Load and return API keys from the .env file."""
    load_dotenv()

    keys = {
        "COINGECKO_KEY": os.getenv("COINGECKO_API_KEY"),
        "IP_QUALITY_KEY": os.getenv("IP_QUALITY_KEY"),
        "GOOGLE_KEY": os.getenv("GOOGLE_API_KEY")
    }
    # Log if a key is missing so you don't crash later
    missing_keys = [k for k, v in keys.items() if not v]
    if missing_keys:
        logger.error(f"⚠️ Critical Keys Missing in .env: {missing_keys}")
        
    return keys

def log_fraud_alert(tx_id, risk_score):
    """Saves a simple log of high-risk transactions."""
    
    risk_percentage = risk_score * 100
    
    # If risk is extremely high (>90%), we elevate to CRITICAL
    if risk_percentage >= 90:
        logger.critical(f"🚨 CRITICAL FRAUD: Tx {tx_id} | Risk: {risk_percentage:.2f}%")
    else:
        logger.warning(f"⚠️ HIGH RISK ALERT: Tx {tx_id} | Risk: {risk_percentage:.2f}%")