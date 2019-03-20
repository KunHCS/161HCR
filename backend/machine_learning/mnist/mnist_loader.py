import keras
import numpy as np
import os
import matplotlib.pyplot as plt
import random


def process_data(input_img):
    return keras.utils.normalize(input_img, axis=1)


def predict_output(input_img):
    index = random.randrange(0, len(input_img))
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'mnist_model.h5')
    model = keras.models.load_model(filename)
    input_data = process_data(input_img)
    plt.imsave(os.path.join(here,'img_out.png'), input_img[index])
    output = np.argmax(model.predict(input_data)[index])
    keras.backend.clear_session()
    return output
