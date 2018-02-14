# coding:utf-8
# code from Deep learning with keras
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.utils import np_utils
from keras.optimizers import SGD

np.random.seed(1671)

def get_mnist_data(reshape, classes_count):
    (x_train, y_train), (x_test, y_test)= mnist.load_data()
    x_train = x_train.reshape(60000, reshape)
    np.divide(x_train, 255, out=x_train, casting="unsafe")
    y_train = np_utils.to_categorical(y_train, classes_count)

    x_test = x_test.reshape(10000, reshape)
    np.divide(x_test, 255, out=x_test, casting="unsafe")
    y_test = np_utils.to_categorical(y_test, classes_count)
    return (x_train, y_train), (x_test, y_test)


def build_model(reshape, classes_count):
    model = Sequential()
    model.add(Dense(classes_count, input_shape=(reshape,)))
    model.add(Activation("softmax"))
    model.summary()
    model.compile(
        loss="categorical_crossentropy",
        optimizer=SGD(),
        metrics=["accuracy"]
    )
    return model



def main(reshap, classes_count):
    (x_train, y_train), (x_test, y_test) = get_mnist_data(reshap, classes_count)
    model = build_model(reshap, classes_count)
    model.fit(x_train, y_train, batch_size=128, verbose=1, validation_split=0.2, epochs=200)
    score = model.evaluate(x_test, y_test, verbose=1)
    print("test score:", score[0])
    print("test accuracy:", score[1])

if __name__ == "__main__":
    reshape = 784
    main(784, 10)
