import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

DATA_DIR = "/tmp/minit"
NUM_STEPS = 1000
MINI_BATCH_SIZE = 100
LOG_DIR = "./logs/softmax/train"

data = input_data.read_data_sets(DATA_DIR, one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y_label = tf.placeholder(tf.float32, [None, 10])

w = tf.Variable(tf.zeros([784, 10]))
y_predict = tf.matmul(x, w)

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(
        logits=y_predict,
        labels=y_label))

tf.summary.histogram("coress entropy", cross_entropy)

gd_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

correct_mask = tf.equal(tf.argmax(y_predict, 1), tf.argmax(y_label, 1))
accuracy = tf.reduce_mean(tf.cast(correct_mask, tf.float32))
tf.summary.histogram("accuracy", accuracy)

config = tf.ConfigProto(log_device_placement=True)
with tf.Session(config=config) as sess:
    sess.run(tf.global_variables_initializer())
    train_writer = tf.summary.FileWriter(LOG_DIR, sess.graph)
    for counter in range(NUM_STEPS):
        merge = tf.summary.merge_all()
        batch_xs, batch_ys = data.train.next_batch(MINI_BATCH_SIZE)
        summary, _ = sess.run([merge, gd_step], feed_dict={x: batch_xs, y_label: batch_ys})
        train_writer.add_summary(summary, counter)

    ans = sess.run(accuracy, feed_dict={x: data.test.images, y_label: data.test.labels})
    print("accuacy: {:.4}%").format(ans * 100)
