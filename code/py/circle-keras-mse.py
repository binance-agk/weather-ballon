import math

from keras import activations
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np

X = np.array([[0], [1], [2], [3], [11], [12]]) / 12
Y = np.array([[0], [1], [2], [3], [11], [12]]) / 12
X = []
Y = []
for t in range(1000):
    x = math.cos(t * math.pi / 50)
    y = math.sin(t * math.pi / 50)
    z = 1
    X.append([x, y])
    Y.append([z])

    r2 = np.random.random()
    X.append([r2 * x, r2 * y])
    Y.append([0])

X = np.array(X)
Y = np.array(Y)
# X = np.array([[12, 12], [0, 12], [0, -12], [12, 0], [-12, 0], [0, 0], [0, 2], [-1, 2], [-11, 11], [11, -11]]) / 12
# y = np.array([[1], [1], [1], [1], [1], [0], [0], [0], [0], [0]])

model = Sequential()
model.add(Dense(15, input_dim=2, activation='tanh'))
model.add(Dense(5, activation='tanh'))
model.add(Dense(1))

sgd = SGD(lr=0.03)
model.compile(loss='mse', optimizer=sgd)

model.fit(X[0:1500], Y[0:1500],
          # validation_data=(X[1501:2000], Y[1501:2000]),
          batch_size=32
          , epochs=500)

# print(model.predict(X))
import matplotlib.pyplot as plt

plt.scatter(X[:, 0], X[:, 1])
plt.show()
