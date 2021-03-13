import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import string
import json

data = input()

def to_tensor(x):
    data_list = list(map(float, x.split()))
    arr = np.array(data_list)
    length = len(arr)
    max_length = 7982
    padded_data = np.zeros(max_length)

    if length < max_length:
        padded_data[0:length] = arr[0:length]
    else:
        padded_data = arr[0:max_length]
    
    return torch.from_numpy(padded_data.astype(np.float32)), torch.tensor(length)

# Hyperparameters
input_size = 26
sequence_length = 307 # 7982(max_length)/26
hidden_size = 256
num_layers = 2
num_classes = 35
learning_rate=0.001

# create a LSTM
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size*sequence_length, num_classes)
    
    def forward(self, x, l):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out_pack, (ht, ct) = self.lstm(x, (h0, c0))
        out_pack = out_pack.reshape(out_pack.shape[0], -1)
        out = self.fc(out_pack)
        return out

def load_checkpoint(checkpoint):
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    model.eval()

# Initialize network
model = LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, num_classes=num_classes)

# initialize optimizer
parameters = filter(lambda p: p.requires_grad, model.parameters())
optimizer = torch.optim.Adam(parameters, lr=learning_rate)

load_checkpoint(torch.load("my_checkpoint.pth.tar"))

sl_class_index = json.load(open('./sl_class_index.json'))

def get_prediction(data):
    tensor = to_tensor(data)
    x = tensor[0]
    l = tensor[1]
    x = x.view(-1, 26).unsqueeze(0)
    _, y_hat = model.forward(x, l).max(1)
    pred_idx = str(y_hat.item())
    return sl_class_index[pred_idx]

print(get_prediction(data))