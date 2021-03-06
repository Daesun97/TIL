# -*- coding: utf-8 -*-
"""2017딥러닝.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/159PGsDlZJbeV8z877GphKFWt7A6ljLYB
"""

import numpy as np
import pickle
def load_mnist(normalize=True, flatten=True, one_hot_label=False):
  def _change_one_hot_label(x): # 라벨을 결정하는것 숫자가 7이라면 7번째 0이 1로 바뀜
    T = np.zeros((x.size, 10))
    for idx ,row in enumerate(T):
      row[x[idx]] = 1
    return T
  

  with open('/content/drive/MyDrive/실습/mnist.pkl의 사본','rb') as f:
    dataset = pickle.load(f)

  if normalize:
    for key in ('train_img', 'test_img'):
      dataset[key] = dataset[key].astype(np.float32)
      dataset[key] /= 255.0

  if one_hot_label:
    dataset['train_label'] = _change_one_hot_label(dataset['train_label'])
    dataset['test_label'] = _change_one_hot_label(dataset['test_label'])



  if not flatten:
    for key in ('train_img','test_img'):
      dataset[key] = dataset[key].reshape(-1,1,28,28) #샘플의 갯수 ,색감체널수, 픽셀의 수28x28
  
  return (dataset['train_img'],dataset['train_label']),(dataset['test_img'],dataset['test_label'])

def cross_entropy_error(y,t):
  if y.ndim ==1: # y의 차원이 1이라면
    t = t.reshape(1,t.size) # 1차원이라 배치를 나눌수 없어서 차원을 나눠줌
    y = y.reshape(1,y.size)

  batch_size = y.shape[0]

  if y.size ==t.size:
    t = t.argmax(axis=1)

  delta = 1e-7
  return -np.sum(np.log(y[np.arange(batch_size), t] +delta)) / batch_size

def sigmoid(x):
  return 1 / (1+np.exp(-x))

def softmax(x): 
  exp_x = np.exp(x)
  sum_exp_x = sum(exp_x)
  y = exp_x / sum_exp_x

  return y

def _numerical_gredient_no_batch(f,x): #편미분해주는것
  h = 1e-4
  grad = np.zeros_like(x)  

  for idx in range(x.size): 
    tmp_val = x[idx]

    #f(x + h)
    x[idx] = float(tmp_val) + h
    fxh1 = f(x)
    
    #f(x - h)

    x[idx] = float(tmp_val) - h
    fxh2 = f(x)

    grad[idx] = (fxh1-fxh2) / (2*h) 
    x[idx] = tmp_val # 원복

  return grad

def numerical_gredient(f, X): #샘플(배치만큼) 가져옴
  if X.ndim == 1:
    return _numerical_gredient_no_batch(f,X)
  else:
    grad = np.zeros_like(X)

    for idx, x in enumerate(X):
      grad[idx] =_numerical_gredient_no_batch(f,x)

    return grad

class TwoLayerNet:
  def __init__(self, input_size,hidden_size,output_size,weight_init_std=0.01):
    self.params = {}
    self.params['W1'] = weight_init_std * np.random.randn(input_size,hidden_size)
    self.params['b1'] = np.zeros(hidden_size)
    self.params['W2'] = np.random.randn(hidden_size, output_size)
    self.params['b2'] = np.zeros(output_size)


  
  def predict(self, x):
    W1, W2 = self.params['W1'],self.params['W2']
    b1, b2 = self.params['b1'],self.params['b2']

    a1 = np.dot(x,W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1,W2) + b2
    y= softmax(a2)

    return y


  def loss(self, x, t):
    y= self.predict(x)
    return cross_entropy_error(y, t)

# 정확도 계산
  def accuracy(self, x, t):
    y = self.predict(x)
    y = np.argmax(y, axis=1)  # y, t는 원핫 형식 -> 라벨형식으로 변경
    t = np.argmax(t, axis=1)

    accuracy = np.sum(y==t) / float(x.shape[0]) #x.shape[0] 는 전체 갯수
    return accuracy

  def numerical_gredient(self, x, t): # 각파라미터 기울기 구하기
    loss_W = lambda W : self.loss(x,t) # 목적함수 - Cross Entropy

    grads = {}
    #목적함수에 대해 각 파라미터별로 편미분한것 
    grads['W1'] = numerical_gredient(loss_W, self.params['W1'])
    grads['b1'] = numerical_gredient(loss_W, self.params['b1'])
    grads['W2'] = numerical_gredient(loss_W, self.params['W2'])
    grads['b2'] = numerical_gredient(loss_W, self.params['b2'])

    return grads

(x_train,y_train),(x_test,y_test)= load_mnist(normalize=True,flatten=True, one_hot_label=True) #데이터 로딩

y_test.shape

network = TwoLayerNet(input_size=784, hidden_size=50,output_size=10) # 2층 신경망 객체 생성

print(network.params['W1'].shape)
print(network.params['b1'].shape)
print(network.params['W2'].shape)
print(network.params['b2'].shape)

x = np.random.rand(50, 784)
y = network.predict(x)
np.argmax(y[0])

iters_num = 10000
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.01 #학습률

train_loss_list = []
train_acc_list = []
test_acc_list=[]

iter_per_epoch = max(train_size/batch_size, 1) #1에폭당 반복 횟수, 최소 한번돌림

for i in range(iters_num):
    batch_mask = np.random.choice(train_size,batch_size) # train_size에서 랜덤하게 숫자를 batch_size만큼 들고옴 , 인덱스
    x_batch = x_train[batch_mask] #랜덤으로 훈련데이터에서 batch_size만큼 선택
    y_batch = y_train[batch_mask]# 얘는 라벨이서

    grad = network.numerical_gredient(x_batch,y_batch) #각 파라미너터의 gradient 계산

    for key in ('W1','b1','W2','b2'):  # 각 파라미터 업데이트
        network.params[key] -=learning_rate * grad[key]


    loss = network.loss(x_batch, y_batch)
    train_loss_list.append(loss) # loss history = 로스값의 경과
    
    train_acc = network.accuracy(x_train, y_train) # 업데이틔 후의 훈련데이터 정확도
    test_acc = network.accuracy(x_test, y_test)# 업데이틔 후의 테스트데이터 정확도
    
    train_acc_list.append(train_acc)
    test_acc_list.append(test_acc)

    print(f"loss {loss}, train_accuracy {train_acc}, test_accuracy {test_acc}")

