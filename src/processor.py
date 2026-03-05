import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def clean_data(self, df):
        """Handle messy API data and create Forensic Flags."""
        # 1. Create Forensic Flags BEFORE filling NaNs (The 'Signal' of missing data)
        df['is_roi_missing'] = df['roi'].isnull().astype(int)
        
        # 2. Convert critical columns to numeric
        cols_to_fix = ['total_volume', 'market_cap', 'current_price', 'high_24h', 'low_24h']
        for col in cols_to_fix:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 3. Strategic Imputation (Fill 0 for Risk, Median for Price)
        risk_cols = ['total_volume', 'market_cap']
        df[risk_cols] = df[risk_cols].fillna(0)
        
        # Fill remaining numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        return df
    
    def engineer_features(self, df):
        """Apply the Forensic EDA findings to the dataset."""
        # Calculate Volatility (The 'Decision DNA' we found in EDA)
        df['price_spread_percentage'] = (df['high_24h'] - df['low_24h']) / (df['low_24h'] + 1e-9)
        
        # High Volume + Low Market Cap = Potential Fraud Signal
        df['volume_mcap_ratio'] = df['total_volume'] / (df['market_cap'] + 1)
        
        # Label the most extreme 5% as 'suspicious' (Threshold Logic)
        limit = df['volume_mcap_ratio'].quantile(0.95)
        df['is_suspicious'] = (df['volume_mcap_ratio'] > limit).astype(int)
        
        # Use logs to squash extreme crypto outliers
        df['log_volume'] = np.log1p(df['total_volume'])
        df['log_mcap'] = np.log1p(df['market_cap'])
        
        return df
    
    def get_graph_data(self, df):
        """
        Creates the Adjacency List for the GNN based on Market Rank.
        Connects each coin to its nearest 3 neighbors in rank.
        """
        edges = []
        df_sorted = df.sort_values('market_cap_rank').reset_index(drop=True)
        
        for i in range(len(df_sorted)):
            for j in range(i + 1, min(i + 4, len(df_sorted))):
                # We store edges as tuples of (Source_Index, Target_Index)
                edges.append([i, j])
                edges.append([j, i]) # GNNs usually want undirected edges (both ways)
                
        return np.array(edges).T # Returns in (2, E) shape for PyTorch Geometric
    
    def scale_features(self, df, features):
        """Normalize features so the GNN learns efficiently."""
        # Ensure only features that exist and have variance are scaled
        active_features = [f for f in features if f in df.columns and df[f].nunique() > 1]
        
        if active_features:
            df[active_features] = self.scaler.fit_transform(df[active_features])
        return df, active_features