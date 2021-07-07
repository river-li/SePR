import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
from model.dataset import qemu_train_data, qemu_validation_data
from scripts.parse_spi_samples import parse_csv
from util.pretty_print import log
import numpy as np
import hiddenlayer as hl

input_size = 32
hidden_size = 500
num_classes = 2


class LinearNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(LinearNN, self).__init__()
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


class FullyConnectedNN(nn.Module):
    def __init__(self):
        super(FullyConnectedNN, self).__init__()
        self.hidden1 = nn.Sequential(nn.Linear(in_features=32, out_features=32, bias=True), nn.ReLU())
        self.hidden2 = nn.Sequential(nn.Linear(in_features=32, out_features=8, bias=True), nn.ReLU())
        self.hidden3 = nn.Sequential(nn.Linear(in_features=8, out_features=2, bias=True), nn.Sigmoid())

    def forward(self, x):
        fc1 = self.hidden1(x)
        fc2 = self.hidden2(fc1)
        output = self.hidden3(fc2)
        return fc1, fc2, output


def train(num_epochs=100, batch_size=64):
    sep, nsep = parse_csv('./data/spi/qemu.csv')
    # del (sep['Unnamed: 0'])
    # del (nsep['Unnamed: 0'])

    sep = np.array(sep)
    nsep = np.array(nsep)

    np.random.shuffle(sep)
    np.random.shuffle(nsep)

    train_sep = sep[:2560, :]
    train_nsep = nsep[:2560, :]

    train_data = np.vstack((train_sep, train_nsep))
    train_label = np.hstack((np.ones(2560, dtype=int), np.zeros(2560, dtype=int)))
    np.random.seed(1234)
    np.random.shuffle(train_data)
    np.random.seed(1234)
    np.random.shuffle(train_label)

    train_data = torch.Tensor(train_data)
    train_label = torch.Tensor(train_label).long()

    model = LinearNN(input_size, hidden_size, num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    total_step = 5120 // batch_size
    for epoch in range(num_epochs):
        for i in range(total_step):
            samples = train_data[i * batch_size:(i + 1) * batch_size]
            labels = train_label[i * batch_size:(i + 1) * batch_size]

            output = model(samples)
            loss = criterion(output, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 10 == 0:
                log('Epoc [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, i + 1, total_step,
                                                                      loss.item()), "YELLOW")

    torch.save(model.state_dict(), "DesneModel.ckpt")
    return model


def main():
    train_loader = DataLoader(dataset=qemu_train_data, batch_size=64, shuffle=True, num_workers=1)
    model = FullyConnectedNN()
    lossFunc = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    epoch_num = 300

    history1 = hl.History()
    for epoch in range(epoch_num):
        for step, (batch_x, batch_y) in enumerate(train_loader):
            _, _, output = model(batch_x)
            train_loss = lossFunc(output, batch_y)
            optimizer.zero_grad()
            train_loss.backward()
            optimizer.step()

            if step % 25 == 0:
                _, _, output = model(qemu_validation_data[0])
                _, predict_label = torch.max(output, 1)
                validation_acc = accuracy_score(qemu_validation_data[1], predict_label)
                log('Epoc [{}/{}], Step [{}], Acc: {}'.format(epoch + 1, epoch_num, step, validation_acc), "YELLOW")
                history1.log(step, train_loss=train_loss, validation_acc=validation_acc)

    torch.save(model.state_dict(), 'FCNN.ckpt')


if __name__ == '__main__':
    main()
