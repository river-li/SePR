import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from scripts.parse_spi_samples import parse_csv
from util.pretty_print import log
import numpy as np
import pandas as pd

input_size = 32
hidden_size = 500
num_classes = 2


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


def train(num_epochs=5,batch_size=64):
    sep, nsep = parse_csv('./data/spi/qemu.csv')
    del (sep['Unnamed: 0'])
    del (nsep['Unnamed: 0'])

    sep = np.array(sep)
    nsep = np.array(nsep)

    np.random.shuffle(sep)
    np.random.shuffle(nsep)

    train_sep = sep[:2560,:]
    train_nsep = nsep[:2560,:]

    train_data = np.vstack((train_sep,train_nsep))
    train_label = np.vstack(np.ones(2560,dtype=int),np.zeors(2560,dtype=int))
    np.random.seed(1234)
    np.random.shuffle(train_data)
    np.random.seed(1234)
    np.random.shuffle(train_label)

    model = DenseNN(input_size, hidden_size, num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    total_step = 5120//batch_size
    for epoch in range(num_epochs):
        for i in range(total_step):
            samples = train_data[i*batch_size:(i+1)*batch_size]
            labels = train_label[i*batch_size:(i+1)*batch_size]

            output = model(samples)
            loss = criterion(output,labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            log('Epoc [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1,num_epochs,i+1,total_step,loss.item()),"YELLOW")

    torch.save(model.state_dict(), "DesneModel.ckpt")
