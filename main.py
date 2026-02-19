import os
import pandas as pd
from src.ingestor import fetch_live_market_data
from src.processor import DataProcessor
from src.gnn_model import run_gnn_pipeline
import pandas as pd

def main():
    print("🚀 Sentinel-Fraud-AI: Starting Automated Pipeline...")

    # Get Data
    df = fetch_live_market_data()
    df.to_csv('data/raw/market_data.csv', index=False)

    # Process Data
    proc = DataProcessor()
    df = proc.clean_data(df)
    df = proc.engineer_features(df)
    df = proc.scale_features(df, ['log_volume', 'log_mcap', 'current_price', 'market_cap_rank'])

    # Train AI
    graph_data, preds = run_gnn_pipeline(df)
    df['ai_prediction'] = preds.numpy()

    # Save final results
    df.to_csv('data/processed/cleaned_market_data.csv', index=False)
    print("✅ Done! Files saved to data/ and models/ folders.")

if __name__ == "__main__":
    main()