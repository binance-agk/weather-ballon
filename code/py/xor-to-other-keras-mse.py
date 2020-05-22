from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np

X = np.array([[0], [1], [2], [3], [11], [12]]) / 12
y = np.array([[0], [1], [2], [3], [11], [12]]) / 12
X = np.array([[0, 12], [0, -12], [12, 0], [-12, 0], [0, 0], [0, 2], [-1, 2], [-11, 11], [11, -11]]) / 12
y = np.array([[1], [0], [0], [3], [11], [12]]) / 12

model = Sequential()
model.add(Dense(2, input_dim=1))

sgd = SGD(lr=0.1)
model.compile(loss='mse', optimizer=sgd)

model.fit(X, y, batch_size=None, epochs=1000)

model.predict(X)
