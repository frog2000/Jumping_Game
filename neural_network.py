import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical, plot_model
import inspect
from game_settings import Settings


def create_nn_model(input_size, num_labels):
    """ Creates a simple vanilla MLP model  """

    hidden_units = 64
    dropout = 0.45

    model = Sequential()
    model.add(Dense(
        hidden_units,
        input_dim=input_size
    ))
    model.add(Activation("relu"))
    model.add(Dropout(dropout))
    model.add(Dense(hidden_units))
    model.add(Activation("relu"))
    model.add(Dropout(dropout))
    model.add(Dense(num_labels))
    model.add(Activation("softmax"))

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
        )
    return model


def train_nn_model(model, obstacle_velocities, obstacle_distances, results):
    """ Trains the MLP model based on the provided obstacle velocities, distances and success/failures of the jumps """

    settings = Settings()
    obstacle_velocities = np.array(obstacle_velocities)
    obstacle_distances = np.array(obstacle_distances)
    results_train = np.array(results)
    results_train = np.reshape(results_train, [results_train.shape[0], -1])
    results_train = to_categorical(results_train, num_classes=2)
    print(results_train)
    obstacle_velocities = obstacle_velocities/100
    obstacle_distances = obstacle_distances/settings.window_width
    inputs_train = np.column_stack((obstacle_velocities, obstacle_distances))
    print(inputs_train.shape)
    print(inputs_train)
    model.fit(inputs_train, results_train, epochs=5)
    return model
