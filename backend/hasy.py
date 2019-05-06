from keras import models, backend, utils
import tensorflow as tf
import numpy as np
import os

print(os.getcwd())
model = models.load_model('alpha_numeric.h5')
graph = tf.get_default_graph()


def predict_hasy(img_input):
    img_input = utils.normalize(img_input)
    with graph.as_default():
        output = model.predict(img_input)
    # backend.clear_session()
    return np.argmax(output[0])


model2 = models.load_model('mnist.h5')


def predict_mnist(img_input):
    img_input = utils.normalize(img_input)
    with graph.as_default():
        output = model2.predict(img_input)
        print(np.argmax(output))
    return np.argmax(output[0])
