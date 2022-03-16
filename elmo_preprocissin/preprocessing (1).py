import numpy as np
import nltk
import ast
import pandas as pd
# 가장 긴 단어의 길이를 맞추고 그 외에는 패딩 단어로 바꿈.
def pad_sequence(sentences, padding_word="<PAD/>"):
    maxlen = max(len(x) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = maxlen - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences

# 단어들을 인덱스로 바꿔줌.
def build_vocab(sentences):
    tokens = [t for d in sentences for t in d]
    text = nltk.Text(tokens, name='NSMC')
    word_count = text.vocab()
    vocabulary_inv = [x[0] for x in word_count.most_common()]
    vocabulary = {x:i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]

def build_input_data(sentences, labels, vocabulary):
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    y = np.array(labels)
    return [x, y]

def load_data():
    
    train = pd.read_csv("./data/train_tokenized.csv",index_col=0)

    sentence = []
    labels = []

    for i,text in enumerate(train['document']):
        sentence.append(ast.literal_eval(text))
        labels.append(train['label'].iloc[i])

    sentence_padded = pad_sequence(sentence)
    vocabulary, vocabulary_inv = build_vocab(sentence_padded)
    x, y = build_input_data(sentence_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]

def batch_iter(data, batch_size, num_epochs):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data) / batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_data = data[shuffle_indices]
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]