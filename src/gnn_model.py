import torch
from torch_geometric.nn import SAGEConv

class FraudGNN(torch.nn.module):
    def __init__(self, in_channels, out_channels):
        super(FraudGNN, self).__init__()
        # Layers that learn from neighboring account behavior
        self.conv1 = SAGEConv(in_channels, 64)
        self.conv2 = SAGEConv(64, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return torch.sigmoid(x) # Returns fraud probability