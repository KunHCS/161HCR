import keras
from .mnist_loader import predict_output


def test_mnist():
    _, (x_test, y_test) = keras.datasets.mnist.load_data()
    return predict_output(x_test)
