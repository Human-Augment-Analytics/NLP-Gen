"""
encoders
"""

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

#the encoder outputs a fixed size vector given an input sequence. The vector used, in the case of an LSTM or RNN, should be its hidden vector, we can control the size of the hidden vector with weight matrices

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first = True)

    def forward(self, x):
        embedded = self.embedding(x)
        output, hidden = self.gru(embedded)
        return output, hidden
