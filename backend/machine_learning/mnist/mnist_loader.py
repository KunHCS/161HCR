from keras.models import load_model
import numpy as np

model = load_model('mnist_model.ht')


def predict_output(input_data):
    return np.argmax(model.predict(input_data)[0])
