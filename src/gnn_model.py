import torch
import torch.nn.functional as F 
from torch_geometric.nn import SAGEConv

class FraudGNN(torch.nn.module):
    def __init__(self, in_channels):
        super(FraudGNN, self).__init__()
        # SAGEConv 'looks' at the neighbors to find fraud rings
        self.conv1 = SAGEConv(in_channels, 16)
        self.conv2 = SAGEConv(16, 1)

    def forward(self, x, edge_index):
        # x = node features, edge_index = connections
        x = self.conv1(x, edge_index)
        x = F.relu()
        x = self.conv2(x, edge_index)
        return torch.sigmoid(x) # Returns probability of fraud (0 to 1)