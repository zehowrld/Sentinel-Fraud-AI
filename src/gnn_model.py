import torch
import torch.nn.functional as F 
from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data

# The Model Architecture
class FraudGNN(torch.nn.module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(FraudGNN, self).__init__()
        # SAGEConv 'looks' at the neighbors to find fraud rings
        self.conv1 = SAGEConv(input_dim, hidden_dim)
        self.conv2 = SAGEConv(hidden_dim, output_dim)

    def forward(self, x, edge_index):
        # x = node features, edge_index = connections
        x = self.conv1(x, edge_index)
        x = F.relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1) # Returns probability of fraud (0 to 1)
    
    # The Training Pipeline
    def train_gnn(df):
        print("🕸️ Building Graph Data Object...")

        # 1. Prepare Features (X) and Labels (y)
        features = ['log_volume', 'log_mcap', 'current_price', 'market_cap_rank']
        x = torch.tensor(df[features].values, dtype=torch.float)
        y = torch.tensor(df['is_suspicious'].values, dtype=torch.long)

        # 2. Create Edges (Connecting coins by Market Rank)
        edge_list = []
        ranks = df['market_cap_rank'].values
        for i in range(len(df)):
            for j in range(i+1, len(df)):
                if abs(ranks[i] - ranks[j]) <= 1:
                    edge_list.append([i,j])
                    edge_list.append([j,i])
        
        edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
        data = Data(x=x, edge_index=edge_index, y=y)

        # 3. Initialize Model
        model = FraudGNN(input_dim= len(features), hidden_dim=16, output_dim=2)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

        # 4. Training Loop
        model.train()
        for epoch in range(51):
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)
            loss = F.nll_loss(out, data.y)
            loss.backward()
            optimizer.step()
            if epoch % 10 == 0:
                print(f"Epoch {epoch} | Loss: {loss.item():.4f}")
        
        # 5. SAVE THE MODEL to your empty 'models/' folder
        torch.save(model.state_dict(), 'models/fraud_model_weights.pth')
        print("✅ Model weights saved to models/fraud_model_weights.pth")
        
        return model, data
