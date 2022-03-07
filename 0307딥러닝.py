# -*- coding: utf-8 -*-
"""0307딥러닝.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nN1032hbua5gvx0fdsZQcj4MTHTgLVnW
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Sequential, Model
tf.random.set_seed(42)

h = [1,0,0,0]
e = [0,1,0,0]
l = [0,0,1,0]
o = [0,0,0,1]

x_data = np.array([[h]], dtype=np.float32 )

x_data.shape

x_data = np.array([[h,e,l,l,o]], dtype=np.float32)
print(x_data.shape)
x_data

hidden_size = 2
cell = layers.SimpleRNNCell(hidden_size)
rnn = layers.RNN(cell, return_sequences=True, return_state=True) #구조를 만듬
outputs,state=rnn(x_data)

print('x_data : {}\t\t\tshape : {}'.format(x_data, x_data.shape))
print('outputs : {}\t\t\tshape : {}'.format(outputs, outputs.shape))
print('state : {}\t\t\tshape : {}'.format(state, state.shape))

x_data = np.array([[h,e,l,l,o],[e,o,l,l,l],[l,l,e,e,l]],dtype=np.float32)
x_data.shape

hidden_size= 2
rnn = layers.SimpleRNN(units=hidden_size, return_sequences=True, return_state=True)
outputs, state = rnn(x_data)

print('x_data : {}\t\t\tshape : {}'.format(x_data, x_data.shape))
print('outputs : {}\t\t\tshape : {}'.format(outputs, outputs.shape))
print('state : {}\t\t\tshape : {}'.format(state, state.shape))

idx2char=['토','마','를','먹','자']

x_data = [[0,0,1,2,4,3]] #토토마를자먹
y_data = [[0,1,0,2,3,4]] #토마토를먹자

num_class=5 #클래스 갯수
input_dim=5 #word_embedding dimension
sequence_length = 6
learning_rate = 0.1

x_one_hot=tf.keras.utils.to_categorical(x_data, num_classes= num_class)
y_one_hot=tf.keras.utils.to_categorical(y_data, num_classes= num_class)

x_one_hot,y_one_hot

x_one_hot.shape,y_one_hot.shape

model = tf.keras.Sequential()
cell = layers.SimpleRNNCell(units=5, input_shape=(sequence_length,input_dim))
model.add(layers.RNN(cell=cell, return_sequences=True,return_state=False,input_shape=(sequence_length,input_dim)))
model.add(layers.TimeDistributed(layers.Dense(units=num_class,activation='softmax')))
# TimeDistributed = 각스탭에서 코스트가 계산되고 각지점에서 오류가 전파됨, 학습레이트가 없음
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),loss='categorical_crossentropy',metrics=['accuracy'])
model.summary()

model.fit(x_one_hot,y_one_hot,epochs=10)

pred=model.predict(x_one_hot)
pred

pred.shape

for i,word in enumerate(pred):
    print(" ".join([idx2char[c] for c in np.argmax(word,axis=1)]))

from tensorflow.keras.preprocessing.text import Tokenizer

sentences = ['i love my dog', 'I, love my cat','You love my dog!']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index #사전화 1부터 시작됨
print(word_index)

from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = ['i love my dog', 'I, love my cat','You love my dog!', 'Do you think my dog is amazing?']
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
print(word_index) 
sequences= tokenizer.texts_to_sequences(sentences)
print(sequences)

padded = pad_sequences(sequences, maxlen=5, padding='post', truncating='post')
print(padded)

from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = ['i love my dog', 'I, love my cat','You love my dog!', 'Do you think my dog is amazing?']
tokenizer = Tokenizer(oov_token="<oov>") #oov_token??= 모르는 단어를 oov토큰으로 만들어 줌
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
print(word_index) 
sequences= tokenizer.texts_to_sequences(sentences)
print(sequences)

test_data = ['i really love my dog', 'my dog loves my manatee']
test_seq = tokenizer.texts_to_sequences(test_data)
padded = pad_sequences(test_seq, maxlen=5, padding='post', truncating='post')

print(padded)

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

tf.random.set_seed(42)

imbd, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)

train_data, test_data = imbd['train'],imbd['test']

train_sentences=[]
test_sentences=[]

train_labels = []
test_labels= []

for s, l in train_data:
    train_sentences.append(s.numpy().decode('utf-8'))
    train_labels.append(l.numpy())
    

for s, l in test_data:
    test_sentences.append(s.numpy().decode('utf-8'))
    test_labels.append(l.numpy())

train_labels = np.array(train_labels)
test_labels= np.array(test_labels)

len(train_sentences),len(train_sentences[0]) #리뷰가25000개, 첫번째 리뷰 알파벳수가 709개

train_sentences[0]

len(test_sentences)

vocab_size = 10000
embedding_dim = 16
max_length = 120 # 인풋의 크기
trunc_type = 'post' #뒤부터 자름
oov_tok = '<oov>'

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_sentences) #사전 만듬

word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(train_sentences) # 숫자의 배열로 변환
padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type) #모든 센텐스 같은크리고 변환

index_word = {value: key for (key,value) in word_index.items()} #사전 밸류와 키값 변환
index_word[1]

padded[0]

def decode_review(text): #사전의 인덱스를 사람이 읽을수 있는것으로 다시 변환 
    return " ".join([index_word.get(i,'?') for i in text]) # 키가 없으면 ?로 나오게함

decode_review(padded[0])

from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_length))
model.add(GlobalAveragePooling1D()) # temporal data를 평균으로 하나로 모아줌
model.add(Dense(6, activation='relu')) #히든레이어
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

test_sequences = tokenizer.texts_to_sequences(test_sentences) # tokenizer는 훈련된 것
test_padd = pad_sequences(test_sequences, maxlen=max_length, truncating=trunc_type)

num_epochs = 10
hist = model.fit(padded,train_labels, validation_data=(test_padd,test_labels), epochs=num_epochs)# 교육된 padd,교육된라벨, 검사할 데이터(test)

embedding_layer= model.layers[0]
weights=embedding_layer.get_weights()[0]
weights.shape

index_word[2]

weights[2] # 'the'의 센텐스 벡터

import matplotlib.pyplot as plt

def plot_graphs(hist,string):
    plt.plot(hist.history[[string]])
    plt.plot(hist.history['val_'+string])
    plt.xlabel('Epochs')
    plt.ylabel(string)
    plt.legend([string,'val_'+string])
    plt.show()

plot_graphs(hist, 'accuracy')
plot_graphs(hist, 'loss')

import matplotlib.pyplot as plt

def plot_graphs(hist, string):
    plt.plot(hist.history[string])
    plt.plot(hist.history['val_'+string])
    plt.xlabel('Epochs')
    plt.ylabel(string)
    plt.legend([string, 'val_'+string])
    plt.show()

plot_graphs(hist, 'accuracy')
plot_graphs(hist, 'loss')

