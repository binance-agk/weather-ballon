from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np

X = np.array([[0], [1], [2], [3], [11], [12]]) / 12
y = np.array([[0], [1], [2], [3], [11], [12]]) / 12

model = Sequential()
model.add(Dense(18, input_dim=1))
model.add(Activation('tanh'))
model.add(Dense(10))
model.add(Activation('sigmoid'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

sgd = SGD(lr=0.01)
model.compile(loss='binary_crossentropy', optimizer=sgd)

model.fit(X, y, batch_size=6, epochs=10000)
