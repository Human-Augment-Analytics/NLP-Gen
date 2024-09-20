import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

import numpy as np
from torch.utils.data import TensorDataset, DataLoader, RandomSampler
SOS_token = 0
class DecoderRNN(nn.Modules):
    def __init__(self, hidden_size, output_size, device, max_len):
        super(DecoderRNN, self).__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first = True)
        self.out = nn.Linear(hidden_size, output_size)
        self.device = device
        self.max_len = max_len

    def forward(self, encoder_outputs, encoder_hidden, target_tensor = None):
        batch_size = encoder_outputs.size(0)
        decoder_input = torch.empty(batch_size, 1, dtype = torch.long, device = device).fill_(SOS_token)

        decoder_hidden = encoder_hidden
        decoder_outputs = []

        for i in range(MAX_LENGTH):
            decoder_output, decoder_hidden = self.forward_step(decoder_input, decoder_hidden)
            decoder_outputs.append(decoder_output)

            if target_tensor is not None:
                decoder_input = target_tensor[:, i].unsqueeze(1)
            else:
                _, topi = decoder_output.topk(1)
                decoder_input = topi.squeeze(-1).detach()

        decoder_outputs = torch.cat(decoder_outputs, dim = 1)
        decoder_outputs = F.log_softmax(decoder_ouputs, dim = -1)
        return decoder_outputs, decoder_hidden, None

    def forward_step(self, x, hidden):
        output = self.embedding(x)
        output = F.relu(output)
        output, hidden = self.gru(output, hidden)
        output = self.out(output)
        return output, hidden

