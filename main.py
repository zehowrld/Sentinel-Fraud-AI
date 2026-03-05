import os
import time
import pandas as pd
from src.ingestor import fetch_live_market_data
from src.processor import DataProcessor
from src.gnn_model import run_gnn_pipeline
from src.agent import run_agent_analysis
from src.utils import logger

def main():
    logger.info("🚀 Sentinel-Fraud-AI: Starting Full Forensic Pipeline...")

    # INGESTION: Fetch raw data
    raw_df = fetch_live_market_data()
    if raw_df is None:
        logger.error("❌ Failed to fetch data. Exiting.")
        return

    # PROCESSING: Apply EDA-driven engineering
    proc = DataProcessor()
    df = proc.clean_data(raw_df)
    df = proc.engineer_features(df)

    # Scale only the features needed for GNN math
    gnn_features = ['log_volume', 'log_mcap', 'current_price', 'market_cap_rank', 
                    'price_spread_percentage', 'is_roi_missing']
    df, scaled_cols = proc.scale_features(df, gnn_features)

    # GNN INFERENCE: Calculate Fraud Probabilities
    # We now return risk_scores (0.0 to 1.0) for the Agent to use
    graph_data, preds, risk_scores= run_gnn_pipeline(df)
    df['ai_prediction'] = preds.numpy()
    df['risk_score'] = risk_scores

    # AGENTIC ANALYSIS: Explaining high-risk tokens
    logger.info("🕵️ Sentinel: Commencing Agentic Forensic Review...")
    
    # Only run the expensive AI Agent on the most suspicious tokens (Top 5)
    suspicious_tokens = df.nlargest(5, 'risk_score')
    
    reports = []
    for _, row in suspicious_tokens.iterrows():
        # Build the forensic state for the Agent
        agent_input = {
            "symbol": row['symbol'],
            "ratio": row['volume_mcap_ratio'],
            "price_volatility": row['price_spread_percentage'],
            "roi_missing": bool(row['is_roi_missing']),
            "is_gnn_flagged": bool(row['ai_prediction']),
            "risk_score": float(row['risk_score'])
        }
        
        try:

            report = run_agent_analysis(agent_input)
            reports.append(report)
            print(f"\n{report}\n")

            time.sleep(4)
        
        except Exception as e:
            logger.warning(f"⚠️ Skipping {row['symbol']} due to API congestion: {e}")


    # Save final results
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/sentinel_forensic_results.csv', index=False)
    
    logger.info(f"✅ Pipeline Complete. Processed {len(df)} tokens.")
    logger.info(f"📁 Reports generated for {len(reports)} high-risk assets.")

if __name__ == "__main__":
    main()