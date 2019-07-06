#encoding=utf-8
import os
import time
import input_data
import numpy as np
import tensorflow as tf
from PIL import Image

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.set_printoptions(linewidth = 600, precision = 3, suppress = False)
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# with tf.device('/gpu:0'):
mnist = input_data.read_data_sets('data/', one_hot= True)

(image_tra, label_tra, num_tra) = (mnist.train.images, mnist.train.labels, mnist.train.num_examples)
(image_tes, label_tes, num_tes) = (mnist.test.images,  mnist.test.labels,  mnist.test.num_examples)

print('\tTrain image: ', image_tra.shape, '\t\tTrain label: ', label_tra.shape,
          '\n\tTest image:  ', image_tes.shape, '\t\tTest label:  ', label_tes.shape)

batch_test_size = 100
num_batch_tra = int(num_tra / batch_test_size)
num_batch_tes = int(num_tes / batch_test_size)

# epsilon = 0.07
num_cn_channel = [1, 64, 128]
num_fc_dimension = [1024, 10]
densel_size = 7 * 7 * 128

strides_cn = {'c1': [1, 1, 1, 1], 'c2': [1, 1, 1, 1]}
strides_pl = {'p1': [1, 2, 2, 1], 'p2': [1, 2, 2, 1]}
ksize_pl =   {'p1': [1, 2, 2, 1], 'p2': [1, 2, 2, 1]}

weight = {
        'wc1': tf.Variable(tf.random_normal([3, 3, num_cn_channel[0], num_cn_channel[1]], stddev = 0.1), dtype = tf.float32),
        'wc2': tf.Variable(tf.random_normal([3, 3, num_cn_channel[1], num_cn_channel[2]], stddev = 0.1), dtype = tf.float32),
        'wf1': tf.Variable(tf.random_normal([7 * 7 * 128, num_fc_dimension[0]], stddev = 0.1), dtype = tf.float32),
        'wf2': tf.Variable(tf.random_normal([num_fc_dimension[0], num_fc_dimension[1]], stddev = 0.1), dtype = tf.float32)
    }

bias = {
        'bc1': tf.Variable(tf.random_normal([num_cn_channel[1]], stddev = 0.1), dtype = tf.float32),
        'bc2': tf.Variable(tf.random_normal([num_cn_channel[2]], stddev = 0.1), dtype = tf.float32),
        'bf1': tf.Variable(tf.random_normal([num_fc_dimension[0]], stddev = 0.1), dtype = tf.float32),
        'bf2': tf.Variable(tf.random_normal([num_fc_dimension[1]], stddev = 0.1), dtype = tf.float32)
    }

def cnn_pool_layer(input, kernal_cn, strides_cn, bias, ksize_pl, strides_pl, keepratio,
                       padding_cn = 'SAME', padding_pl = 'SAME'):
    out_cn = tf.nn.conv2d(input, kernal_cn, strides = strides_cn, padding = padding_cn)
    out_ac = tf.nn.relu(tf.nn.bias_add(out_cn, bias))
    out_pl = tf.nn.max_pool(out_ac, ksize = ksize_pl, strides = strides_pl, padding = padding_pl)
    out_dp = tf.nn.dropout(out_pl, keepratio)
    out = {'cn': out_cn, 'ac': out_ac, 'pl': out_pl, 'dp': out_dp}
    return out

def fc_layer(input, weight, bias, keepratio, acfun = 'False'):
    out_pre = tf.add(tf.matmul(input, weight), bias)
    if acfun == 'relu':
        out_ac = tf.nn.relu(out_pre)
    elif acfun == 'sigmoid':
        out_ac = tf.nn.sigmoid(out_pre)
    elif acfun == 'tanh':
        out_ac = tf.nn.tanh(out_pre)
    else:
        out_ac = tf.add(tf.matmul(input, weight), bias)
    out_dp = tf.nn.dropout(out_ac, keepratio)
    out = {'ac': out_ac, 'dp': out_dp}
    return out

x = tf.placeholder(tf.float32, [None, image_tra.shape[1]])
y = tf.placeholder(tf.float32, [None, label_tra.shape[1]])
keepratio = tf.placeholder(tf.float32)
c1_in  = tf.reshape(x, [-1, 28, 28, 1])
c1_out = cnn_pool_layer(c1_in,  weight['wc1'], strides_cn['c1'], bias['bc1'], ksize_pl['p1'], strides_pl['p1'],
                            keepratio = keepratio, padding_cn = 'SAME', padding_pl = 'SAME')['dp']
c2_out = cnn_pool_layer(c1_out, weight['wc2'], strides_cn['c2'], bias['bc2'], ksize_pl['p2'], strides_pl['p2'],
                            keepratio = keepratio, padding_cn = 'SAME', padding_pl = 'SAME')['dp']
f1_in = tf.reshape(c2_out, [-1, weight['wf1'].get_shape().as_list()[0]])
f1_out = fc_layer(f1_in,  weight['wf1'], bias['bf1'], keepratio, acfun = 'relu')['dp']
f2_out = fc_layer(f1_out, weight['wf2'], bias['bf2'], keepratio, acfun = 'False')['ac']

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = f2_out, labels = y))
gradient = tf.gradients(loss, x)

pred = tf.nn.softmax(f2_out)
corr = tf.equal(tf.argmax(f2_out, 1), tf.argmax(y, 1))
accu = tf.reduce_mean(tf.cast(corr, tf.float32))

saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, './model_save/model_500epo.ckpt')
    accu_tra, accu_tes = 0, 0
    grad_ADE_tra, grad_ADE_tes = np.empty([0, 784]), np.empty([0, 784])
    _label_tra, _label_tes = np.empty([0, 10]), np.empty([0, 10])
    index_epsilon = 0
    time_st = time.time()
    for index_tra in range(num_batch_tra):
        image_batch_tra, label_batch_tra = mnist.train.next_batch(batch_test_size)
        accu_tra += sess.run(accu, feed_dict={x: image_batch_tra, y: label_batch_tra, keepratio: 1.0}) / num_batch_tra
    for index_tes in range(num_batch_tes):
        image_batch_tes, label_batch_tes = mnist.train.next_batch(batch_test_size)
        accu_tes += sess.run(accu, feed_dict={x: image_batch_tes, y: label_batch_tes, keepratio: 1.0}) / num_batch_tes
    time_ed = time.time()
    print('Accuracy on Clean Example:\t\tTrain/Test\t%-6.4f/%-6.4f\t\tCost Time\t%-6.4f'
          % (accu_tra, accu_tes, time_ed - time_st))

    for epsilon in range(1, 21):
        epsilon /= 100.0
        index_epsilon += 1
        accu_ADE_tra, accu_ADE_tes = 0, 0
        time_st = time.time()
        for _index_tra in range(num_batch_tra):
            image_batch_tra, label_batch_tra = mnist.train.next_batch(batch_test_size)
            grad_batch_tra = np.squeeze(np.array(sess.run(gradient,
                 feed_dict = {x: image_batch_tra, y: label_batch_tra, keepratio: 1.0})), axis = 0)
            ADE_batch_tra = image_batch_tra + epsilon * np.sign(grad_batch_tra)
            accu_ADE_tra += sess.run(accu, feed_dict = {x: ADE_batch_tra, y: label_batch_tra, keepratio: 1.0}) / num_batch_tra
        for _index_tes in range(num_batch_tes):
            image_batch_tes, label_batch_tes = mnist.train.next_batch(batch_test_size)
            grad_batch_tes = np.squeeze(np.array(sess.run(gradient,
                 feed_dict = {x: image_batch_tes, y: label_batch_tes, keepratio: 1.0})), axis = 0)
            ADE_batch_tes = image_batch_tes + epsilon * np.sign(grad_batch_tes)
            accu_ADE_tes += sess.run(accu, feed_dict={x: ADE_batch_tes, y: label_batch_tes, keepratio: 1.0}) / num_batch_tes
        time_ed = time.time()

        image_save, label_save = mnist.train.next_batch(1)
        print('Clean \t', np.argmax(label_save), sess.run(pred, feed_dict={x: image_save, y: label_save, keepratio: 1.0}))
        for i in range(20):
            grad_save = np.squeeze(np.array(sess.run(gradient,
                 feed_dict = {x: image_tes[0].reshape([-1, 784]), y: label_tes[0].reshape([-1, 10]), keepratio: 1.0})), axis = 0)
            ADE_save = np.add(image_tes[0], (i+1) * 0.01 * np.sign(grad_save))
            pred_np = sess.run(pred, feed_dict = {x: ADE_save, y: label_save, keepratio: 1.0})
            print('Attack\t', np.argmax(pred_np), pred_np)
        img = Image.fromarray(ADE_save.reshape([28, 28]) * 255).convert('L')
        img.save('save/attack%s.jpg' % str(index_epsilon).zfill(3))
        #print(ADE_save, type(ADE_save))
        img = Image.fromarray(ADE_save)
        print('Attack Turn%s (ε= %-4.2f):    \tTrain/Test\t%-6.4f/%-6.4f\t\tCost Time\t%-6.4f'
              % (str(index_epsilon).zfill(3), epsilon, accu_ADE_tra, accu_ADE_tes, time_ed - time_st))



