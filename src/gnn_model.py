import torch
import torch.nn.functional as F 
from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data
import os

# The Model Architecture
class FraudGNN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(FraudGNN, self).__init__()
        # SAGEConv 'looks' at the neighbors to find fraud rings
        self.conv1 = SAGEConv(input_dim, hidden_dim)
        self.conv2 = SAGEConv(hidden_dim, output_dim)

    def forward(self, x, edge_index):
        # x = node features, edge_index = connections
        # Layer 1
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.3, training=self.training)

        # Layer 2
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1) # Returns probability of fraud (0 to 1)
    
# The Training Pipeline
def run_gnn_pipeline(df):
        print("🕸️ Building Graph Data Object...")

        # 1. Feature Selection (Based on EDA Findings)
        # We include 'price_spread_percentage' as it was our 2nd most important feature

        features = [
            'log_volume', 'log_mcap', 'current_price', 
            'market_cap_rank', 'price_spread_percentage', 'is_roi_missing'
        ]

        # Convert to Tensors
        x = torch.tensor(df[features].values, dtype=torch.float)
        y = torch.tensor(df['is_suspicious'].values, dtype=torch.long)

        # 2. Create Edges (Connecting each coin to its 3 closest market-rank neighbors)
        edge_list = []
        
        for i in range(len(df)):
            # Connect to 3 neighbors ahead to create a robust 'Market Segment'
            for j in range(i+1, min(i + 4, len(df))):
                    edge_list.append([i,j])
                    edge_list.append([j,i]) # Undirected edges
        
        edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
        data = Data(x=x, edge_index=edge_index, y=y)

        # Dynamic Class Weighting (Handles Imbalance)
        num_fraud = (y == 1).sum().item()
        num_clean = (y == 0).sum().item()

        # If no fraud is found in the current batch, use default weights
        if num_fraud > 0:
            # We weigh fraud higher because it's rare (Anomalous)
            weight_for_fraud = num_clean / num_fraud
            weights = torch.tensor([1.0, weight_for_fraud], dtype=torch.float)
        else:
            weights = torch.tensor([1.0, 5.0], dtype=torch.float)
        

        # 3. Initialize Model
        model = FraudGNN(input_dim= len(features), hidden_dim=32, output_dim=2)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

        # 4. Training Loop
        model.train()
        for epoch in range(101):
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)

            # USE WEIGHTED LOSS
            loss = F.nll_loss(out, data.y, weight=weights)

            loss.backward()
            optimizer.step()
            if epoch % 25 == 0:
                print(f"🔹 Epoch {epoch:3d} | Loss: {loss.item():.4f}")

        # 5. Generate Predictions & Risk Scoring
        model.eval()
        with torch.no_grad():
            logits = model(data.x, data.edge_index)
            # Convert log_softmax back to 0.0-1.0 probability
            probabilities = torch.exp(logits) 
            risk_scores = probabilities[:, 1].numpy() # Probability of class '1' (Suspicious)
            predictions = logits.argmax(dim=1)

        # 6. SAVE THE MODEL to your empty 'models/' folder
        os.makedirs('models', exist_ok=True)
        torch.save(model.state_dict(), 'models/fraud_model_weights.pth')
        print(f"✅ Sentinel Model Saved. High-Risk Anomalies Detected: {predictions.sum().item()}")

        # We return risk_scores so the Agent can explain them
        return data, predictions, risk_scores
