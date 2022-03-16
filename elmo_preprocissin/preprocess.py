import os
import re
import json

import numpy as np
import pandas as pd
from tqdm import tqdm

from konlpy.tag import Okt

FILTERS =  "[~.,!?\"':;)(]"
CHANGE_FILTER = re.compile(FILTERS)
PAD = "<PAD>"
SOS = "<SOS>"
EOS = "<EOS>"
UNK = "<UNK>"

PAD_INDEX = 0
SOS_INDEX = 1
EOS_INDEX = 2
UNK_INDEX = 3

MARKER = [PAD, SOS, EOS, UNK]

MAX_SEQUENCE = 25

def load_data(path):
    data_df = pd.read_csv(path)
    question, answer = list(data_df['Q']), list(data_df['A'])
    return question, answer


def prepro_like_morphlized(data):
    morph_analyzer = Okt()
    result_data = []
    for seq in tqdm(data):
        result_data.append(" ".join(morph_analyzer.morphs(seq)))
    return result_data

def data_tokenizer(data):
    words = []
    for sentence in data:
        sentence = re.sub(CHANGE_FILTER, "", sentence)
        for word in sentence.split():
            if word:
                words.append(word)
    return list(set(words))

def make_vocabulary(vocabulary_list):
    char2idx = { char: idx for idx, char in enumerate(vocabulary_list)}
    idx2char = { idx : char for idx, char in enumerate(vocabulary_list)}

    return char2idx, idx2char

def load_vocabulary(path, vocab_path, tokenize_as_morph=False):
    vocabulary_list = []
    if not os.path.exists(vocab_path):
        if os.path.exists(path):
            question, answer = load_data(path)
            if tokenize_as_morph:
                question = prepro_like_morphlized(question)
                answer = prepro_like_morphlized(answer)

            words = data_tokenizer(question + answer)
            words[:0] = MARKER
            
            with open(vocab_path, 'w', encoding='utf-8') as vocabulary_file:
                for word in words:
                    vocabulary_file.write(word + '\n')

    with open(vocab_path, 'r', encoding='utf-8') as vocabulary_file:
        for line in vocabulary_file:
            vocabulary_list.append(line.strip())

    char2idx, idx2char = make_vocabulary(vocabulary_list)

    return char2idx, idx2char, len(char2idx)

def enc_processing(value, dictionary, tokenize_as_morph=False):
    sequence_input_index = []
    sequence_length = []

    if tokenize_as_morph:
        value = prepro_like_morphlized(value)

    for sequence in value:
        sequence = re.sub(CHANGE_FILTER, "", sequence)
        sequence_index = []

        for word in sequence.split():
            if dictionary.get(word):
                sequence_index.append(dictionary[word])
            else:
                sequence_index.append(dictionary[UNK])
        
        #truncating
        if len(sequence_index) > MAX_SEQUENCE:
            sequence_index = sequence_index[:MAX_SEQUENCE]
        
        sequence_length.append(len(sequence_index))
        
        #padding
        sequence_index += (MAX_SEQUENCE - len(sequence_index)) * [dictionary[PAD]]

        sequence_input_index.append(sequence_index)

    return np.asarray(sequence_input_index), sequence_length

def dec_output_processing(value, dictionary, tokenize_as_morph=False):
    sequence_output_index = []
    sequence_length = []

    if tokenize_as_morph:
        value = prepro_like_morphlized(value)

    for sequence in value:
        sequence = re.sub(CHANGE_FILTER, "", sequence)
        sequence_index = []

        for word in sequence.split():
            if dictionary.get(word):
                sequence_index.append(dictionary[word])
            else:
                sequence_index.append(dictionary[UNK])

        sequence_index.insert(0, dictionary[SOS])
        
        #truncating
        if len(sequence_index) > MAX_SEQUENCE:
            sequence_index = sequence_index[:MAX_SEQUENCE]
        
        sequence_length.append(len(sequence_index))
        
        #padding
        sequence_index += (MAX_SEQUENCE - len(sequence_index)) * [dictionary[PAD]]

        sequence_output_index.append(sequence_index)

    return np.asarray(sequence_output_index), sequence_length

def dec_target_processing(value, dictionary, tokenize_as_morph=False):
    sequence_target_index = []

    if tokenize_as_morph:
        value = prepro_like_morphlized(value)

    for sequence in value:
        sequence = re.sub(CHANGE_FILTER, "", sequence)
        sequence_index = []

        for word in sequence.split():
            if dictionary.get(word):
                sequence_index.append(dictionary[word])
            else:
                sequence_index.append(dictionary[UNK])
        
        #truncating
        if len(sequence_index) > MAX_SEQUENCE:
            sequence_index = sequence_index[:MAX_SEQUENCE - 1] + [dictionary[EOS]]
        else:
            sequence_index.append(dictionary[EOS])

        
        #padding
        sequence_index += (MAX_SEQUENCE - len(sequence_index)) * [dictionary[PAD]]

        sequence_target_index.append(sequence_index)

    return np.asarray(sequence_target_index)