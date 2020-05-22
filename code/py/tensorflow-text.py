import math
import random

from keras import Sequential
from keras.layers import Dense
import numpy as np

train = [2.00, 3.0, 5.0, 6.00]
train = np.array(train) / 6.0

train_labels = [ 2.00,3.0, 5.0, 6.00]
train_labels = np.array(train_labels) / 6.0
model = Sequential([
    Dense(2, activation='relu', input_shape=(1,)),
    # Dense(3, activation='relu'),
    Dense(1, activation='sigmoid'),
])

# Compile the model.
model.compile(
    optimizer='adam',
    loss='mse'
)

# Train the model.
model.fit(
    train,
    train_labels,
    epochs=310,
    batch_size=None
)

# Evaluate the model.
# model.evaluate(
#     test_images,
#     to_categorical(test_labels)
# )

# Save the model to disk.
# model.save_weights('model.h5')

# Load the model from disk later using:
# model.load_weights('model.h5')

# Predict on the first 5 test images.
predictions = model.predict(train)
