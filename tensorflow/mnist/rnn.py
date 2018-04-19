import tensorflow as tf
import os
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/mnist", one_hot=True)
log_dir = "/tmp/rnn_mnist_log"
time_steps = 28
element_size = 28
batch_size = 128
hidden_layer_size = 128
num_classes = 10


def var_summaries(var):
    with tf.name_scope("summaries"):
        mean = tf.reduce_mean(var)
        tf.summary.scalar("mean", mean)
        with tf.name_scope("std_dev"):
            std_dev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar("std_dev", std_dev)
        tf.summary.scalar("max", tf.reduce_max(var))
        tf.summary.scalar("min", tf.reduce_min(var))
        tf.summary.histogram("histogram", var)


def rnn_cell():
    with tf.name_scope("rnn_weights"):
        with tf.name_scope("W_x"):
            wx = tf.Variable(tf.zeros([element_size, hidden_layer_size]))
            var_summaries(wx)

        with tf.name_scope("W_h"):
            wh = tf.Variable(tf.zeros([hidden_layer_size, hidden_layer_size]))
            var_summaries(wh)

        with tf.name_scope("bias"):
            b_rnn = tf.Variable(tf.zeros(hidden_layer_size))
            var_summaries(b_rnn)
    return wx, wh, b_rnn


def rnn_model():
    x_shape = [None, time_steps, element_size]
    y_shape = [None, num_classes]
    hidden_state_shape = [batch_size, hidden_layer_size]

    x = tf.placeholder(tf.float32, shape=x_shape, name="inputs")
    y = tf.placeholder(tf.float32, shape=y_shape, name="labels")
    processed_input = tf.transpose(x, perm=[1, 0, 2])

    init_hidden = tf.zeros(hidden_state_shape)
    wx, wh, b_rnn = rnn_cell()

    def rnn_step(previos_hidden_state, x):
        return tf.tanh(tf.matmul(previos_hidden_state, wh) + tf.matmul(x, wx) + b_rnn)

    all_hiden_states = tf.scan(rnn_step, processed_input, initializer=init_hidden, name="states")

    with tf.name_scope("linear_layer_weights"):
        with tf.name_scope("linear_w"):
            shape = [hidden_layer_size, num_classes]
            wl = tf.Variable(tf.truncated_normal(shape, mean=0, stddev=.01))
            var_summaries(wl)

        with tf.name_scope("linear_bias"):
            shape = [num_classes]
            bl = tf.Variable(tf.truncated_normal(shape=shape, mean=0, stddev=.01))

    def get_linear_layer(hidden_state):
        return tf.matmul(hidden_state, wl) + bl

    with tf.name_scope("linear_layer_weights"):
        all_outputs = tf.map_fn(get_linear_layer, all_hiden_states)
        output = all_outputs[-1]
        tf.summary.histogram("outputs", output)

    with tf.name_scope("loss"):
        loss = tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y)
        loss = tf.reduce_mean(loss)
        tf.summary.scalar("loss", loss)

    with tf.name_scope("train"):
        opt = tf.train.RMSPropOptimizer(0.001, 0.9)
        train_op = opt.minimize(loss)

    with tf.name_scope("accuracy"):
        accuracy = tf.equal(tf.argmax(y, 1), tf.argmax(output, 1))
        accuracy = tf.cast(accuracy, tf.float32)
        accuracy = tf.reduce_mean(accuracy)
        accuracy = accuracy * 100.0
        tf.summary.scalar("accuracy", accuracy)

    summary = tf.summary.merge_all()
    return x, y, train_op, accuracy, summary, loss

def train():
    shape = [-1, time_steps, element_size]
    test_data = mnist.test.images[:batch_size].reshape(shape)
    test_label = mnist.test.labels[:batch_size]

    x, y, train_op, accuracy, summary, loss = rnn_model()

    train_log_dir = os.path.join(log_dir, "train")
    train_writer = tf.summary.FileWriter(train_log_dir, graph=tf.get_default_graph())

    test_log_dir = os.path.join(log_dir, "test")
    test_writer = tf.summary.FileWriter(test_log_dir, graph=tf.get_default_graph())

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(10 * 1000):
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            x_shape = [batch_size, time_steps, element_size]
            batch_x = batch_x.reshape(x_shape)
            feed_dict = {x: batch_x, y: batch_y}
            fetched_summary, _ = sess.run([summary, train_op], feed_dict=feed_dict)
            train_writer.add_summary(fetched_summary, i)

            if i % 100 == 0:
                fetched_accuracy, fetched_loss = sess.run([accuracy, loss], feed_dict=feed_dict)
                print("iter: {}, loss: {}, acc: {}".format(i, fetched_loss, fetched_accuracy))

            if i % 10 == 0:
                fetched_summary, fetched_accuracy = sess.run([summary, accuracy], feed_dict={x: test_data, y: test_label})
                test_writer.add_summary(fetched_summary, i)

        test_acc = sess.run(accuracy, feed_dict={x: test_data, y: test_label})
        print("test accuracy: {}".format(test_acc))

if __name__ == "__main__":
    train()
