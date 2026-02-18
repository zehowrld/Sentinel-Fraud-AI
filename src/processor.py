import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class Dataprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def clean_data(self, df):
        # Convert columns to numbers to handle messy API data
        for col in ['total_volume', 'market_cap', 'current_price']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill empty spots with the median (keeps data stable)
            return df.fillna(df.median(numeric_only=True))
        
    def engineer_features(self, df):
        # High Volume + Low Market Cap = Potential Fraud Signal
        df['volume_mcap_ratio'] = df['total_volume']/ (df['market_cap'] + 1)
        # Label the most extreme 5% as 'suspicious' for the AI to study
        limit = df['volume_mcap_ratio'].quantile(0.95)
        df['is_suspicious'] = (df['volume_mcap_ratio'] > limit).astype(int)
        # Use logs to make the numbers easier for the AI to read
        df['log_volume'] = np.log1p(df['total_volume'])
        df['log_mcap'] = np.log1p(df['market_cap'])
        return df
    
    def scale_features(self, df, features):
        # Normalize so large numbers don't confuse the AI
        df[features] = self.scaler.fit_transform(df['features'])
        return df