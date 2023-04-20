from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from pathlib import Path

PATH = Path(__file__).parents[0]


def create_uneducated_predictor(input_shape: tuple, outputs: int, neurons_per_hidden_layer: list[int], activation: str = "relu", last_activation: str = "softmax") -> Model:
    predictor_input = Input(input_shape)
    x = predictor_input
    for neurons in neurons_per_hidden_layer:
        x = Dense(neurons, activation=activation)(x)
    x = Dense(outputs, activation=last_activation)(x)
    return Model(predictor_input, x)
