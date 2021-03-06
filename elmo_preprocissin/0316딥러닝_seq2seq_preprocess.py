# -*- coding: utf-8 -*-
"""0316딥러닝_seq2seq_preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZsmhMYOI78NiX1UA0VY5ZFVZD5L0y4bY

ELMO preprocessin
"""

! pip install konlpy

import sys
sys.path.append("/content/drive/MyDrive/실습")
from preprocess import *

PATH="/content/drive/MyDrive/실습/data/ChatBotData.csv_short"
VOCAB_PATH="/content/drive/MyDrive/실습/data/vocabulary.txt"

inputs, outputs = load_data(PATH)



char2idx, idx2char, vocab_size = load_vocabulary(PATH, VOCAB_PATH, tokenize_as_morph=True)

index_inputs, input_seq_len = enc_processing(inputs, char2idx, tokenize_as_morph=False)
index_outputs, output_seq_len = dec_output_processing(outputs, char2idx, tokenize_as_morph=False)
index_targets = dec_target_processing(outputs, char2idx, tokenize_as_morph=False)

data_configs = {}
data_configs['char2idx'] = char2idx
data_configs['idx2char'] = idx2char
data_configs['vocab_size'] = vocab_size
data_configs['pad_symbol'] = PAD
data_configs['sos_symbol'] = SOS
data_configs['eos_symbol'] = EOS
data_configs['unk_symbol'] = UNK

import numpy as np
import json

DATA_IN_PATH = '/content/drive/MyDrive/실습/data/'
TRAIN_INPUTS = 'train_inputs.npy'
TRAIN_OUTPUTS = 'train_outputs.npy'
TRAIN_TARGETS = 'train_targets.npy'
DATA_CONFIGS = 'data_configs.json'

np.save(open(DATA_IN_PATH + TRAIN_INPUTS, 'wb'), index_inputs)
np.save(open(DATA_IN_PATH + TRAIN_OUTPUTS , 'wb'), index_outputs)
np.save(open(DATA_IN_PATH + TRAIN_TARGETS , 'wb'), index_targets)

json.dump(data_configs, open(DATA_IN_PATH + DATA_CONFIGS, 'w'))

