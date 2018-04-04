import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

DATA_DIR = "/tmp/minit"
NUM_STEPS = 1000
MINI_BATCH_SIZE = 100


class GraphBuilder(object):
    @classmethod
    def weigth_variable(cls, shape):
        init = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(init)

    @classmethod
    def bias_variable(cls, shape):
        init = tf.constant(0.1, shape=shape)
        return tf.Variable(init)

    @classmethod
    def conv2d(cls, x, w):
        return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding="SAME")

    @classmethod
    def max_pool_2x2(cls, x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    @classmethod
    def conv_layer(cls, x, shape):
        w = cls.weigth_variable(shape)
        b = cls.bias_variable([shape[3]])
        return tf.nn.relu(cls.conv2d(x, w) + b)

    @classmethod
    def full_layer(cls, x, size):
        in_size = int(x.get_shape()[1])
        w = cls.weigth_variable([in_size, size])
        b = cls.bias_variable([size])
        return tf.matmul(x, w) + b

    @classmethod
    def build_model(cls):
        x = tf.placeholder(tf.float32, shape=[None, 28 * 28])
        y = tf.placeholder(tf.float32, shape=[None, 10])

        image = tf.reshape(x, [-1, 28, 28, 1])
        conv1 = cls.conv_layer(image, shape=[5, 5, 1, 32])
        conv1_pool = cls.max_pool_2x2(conv1)

        conv2 = cls.conv_layer(conv1_pool, shape=[5, 5, 32, 64])
        conv2_pool = cls.max_pool_2x2(conv2)

        conv2_flat = tf.reshape(conv2_pool, [-1, 7 * 7 * 64])
        full_1 = tf.nn.relu(cls.full_layer(conv2_flat, 1024))

        keep_prob = tf.placeholder(tf.float32)
        full1_drop = tf.nn.dropout(full_1, keep_prob=keep_prob)

        predict_y = cls.full_layer(full1_drop, 10)

        return x, y, keep_prob, predict_y


def train_mnist(batch_size=50, steps=1000, learning_rate=1e-4):
    mnist = input_data.read_data_sets(DATA_DIR, one_hot=True)

    x, y, keep_prob, predict_y = GraphBuilder.build_model()
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predict_y, labels=y))
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    correct_predict = tf.equal(tf.argmax(predict_y, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # training
        for step  in range(steps):
            batch = mnist.train.next_batch(batch_size)
            if step % 10 == 0:
                train_accuracy = sess.run(accuracy, feed_dict={
                    x: batch[0],
                    y: batch[1],
                    keep_prob: 1
                })
                print("step {}, train accuracy: {}".format(step, train_accuracy))
            feed_dict = {
                x: batch[0],
                y: batch[1],
                keep_prob: 0.5
            }
            sess.run(train_step, feed_dict=feed_dict)

        # test
        test_x = mnist.test.images.reshape(10, 1000, 28 * 28)
        test_y = mnist.test.labels.reshape(10, 1000, 10)
        test_acs = [
            sess.run(
                accuracy,
                feed_dict={x: test_x[i], y: test_y[i], keep_prob: 1.0})
            for i in range(10)]
        test_ac = np.mean(test_acs)
        print("test accuracy: {}".format(test_ac))


if __name__ == "__main__":
    train_mnist()
