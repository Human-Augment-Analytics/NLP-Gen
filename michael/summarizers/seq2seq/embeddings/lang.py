import unicodedata
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

import numpy as np
from torch.utils.data import TensorDataset, DataLoader, RandomSampler

def unicodeToAscii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z!?]+", r" ", s)
    return s.strip()

#read translation data, where each line is an english statement and a spanish statement separated by a tab
def readLangs(path):
    print('Reading lines...')

    lines = open(path, encoding = 'utf-8').read().strip().split('\n')
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    input_lang = Lang()
    output_lang = Lang()

    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])

    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs

#Lang class from https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html#visualizing-attention
class Lang:
    def __init__(self):
        self.word2index = {}
        self.wordcount = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2

    def addSentece(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.wordcount[word] = 1
            self.index2word[self.n_words] = word
            self.n_words = self.n_words + 1
        else:
            self.wordcount[word] += 1
    
        
