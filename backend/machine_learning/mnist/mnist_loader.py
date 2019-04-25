import keras
import numpy as np
import os
import matplotlib.pyplot as plt
import random


def process_data(input_img):
    return input_img


def predict_output(input_img):
    index = random.randrange(0, len(input_img))
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'mnist_model.h5')
    model = keras.models.load_model(filename)
    input_data = process_data(input_img)
    output = np.argmax(model.predict(input_data)[0])
    keras.backend.clear_session()
    return output
