import torch
import torch.nn as nn
import numpy as np
import pandas as pd

input_size = 28 * 28
hidden_size = 500
num_classes = 10

class DenseNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(DenseNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        out = self.fc1(x)
        out = self.dropout(out)
        out = self.relu(out)
        out = self.fc2(out)
        return out

model = DenseNN(input_size, hidden_size, num_classes)
model.train()
model.eval()