import os 
import logging
from dotenv import load_dotenv

# Initialize logging to see what's happening in terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_env_keys():
    """Load and return API keys from the .env file."""
    load_dotenv()
    return {
        "COINGECKO_KEY": os.getenv("COINGECKO_API_KEY"),
        "IP_QUALITY_KEY": os.getenv("IP_QUALITY_KEY"),
        "OPENAI_KEY"": os.getenv("OPENAI_API_KEY")       
        
    }
    return keys

def log_fraud_alert(tx_id, risk_score):
    """Saves a simple log of high-risk transactions."""
    logger.warning(f"🚨 FRAUD ALERT: Transaction {tx_id} flagged with {risk_score*100}% risk!")