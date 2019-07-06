import os
import time
import input_data
import numpy as np
import tensorflow as tf

# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"]="0"

# with tf.device('/gpu:0'):
mnist = input_data.read_data_sets('data/', one_hot= True)
(image_tra, label_tra, num_tra) = (mnist.train.images, mnist.train.labels, mnist.train.num_examples)
(image_tes, label_tes, num_tes) = (mnist.test.images,  mnist.test.labels,  mnist.test.num_examples)
print('\tTrain image: ', image_tra.shape, '\t\tTrain label: ', label_tra.shape,
      '\n\tTest image:  ', image_tes.shape, '\t\tTest label:  ', label_tes.shape)
lr = 1e-3
num_epoch = 500
num_epoch_display = 10
batch_size = 128
batch_test_size = 100
num_batch = int(num_tra / batch_size)
num_batch_test = int(num_tra / batch_test_size)
time_st = time.time()
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
# f2_out = conv_basic(x, weight, bias, keepratio)['out']
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = f2_out, labels = y))
train_step = tf.train.AdadeltaOptimizer(lr).minimize(loss)
pred = tf.nn.softmax(f2_out)
corr = tf.equal(tf.argmax(f2_out, 1), tf.argmax(y, 1))
accu = tf.reduce_mean(tf.cast(corr, tf.float32))


# gpu_fraction = 0.1
# gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    print('***Start***')

    for index_epoch in range(num_epoch):
        if (index_epoch + 1) % num_epoch_display == 1:
            time_st = time.time()

        loss_tra, loss_tes, accu_tra, accu_tes = 0, 0, 0, 0
        for index_batch in range(num_batch):
            image_batch, label_batch = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict = {x: image_batch, y: label_batch, keepratio: 0.7})
            loss_tra += sess.run(loss, feed_dict = {x: image_batch, y: label_batch, keepratio: 1.0}) / num_batch

        for index_test in range(num_batch_test):
            image_batch, label_batch = mnist.train.next_batch(batch_test_size)
            loss_tes += sess.run(loss, feed_dict = {x: image_batch, y: label_batch, keepratio: 1.0}) / num_batch_test
            accu_tra += sess.run(accu, feed_dict = {x: image_batch, y: label_batch, keepratio: 1.0}) / num_batch_test
            accu_tes += sess.run(accu, feed_dict = {x: image_batch, y: label_batch, keepratio: 1.0}) / num_batch_test

        if (index_epoch + 1) % num_epoch_display == 0:
            time_ed = time.time()
            print('Epoch: %s/%s\tTrain acc: %-6.4f\tTest acc: %-6.4f\tCost time: %-6.4f'
                  % (str(index_epoch + 1).zfill(3), str(num_epoch).zfill(3), accu_tra, accu_tes, (time_ed - time_st)))

    model_path = saver.save(sess, 'model_save\model_500epo.ckpt')
    print('Model has been saved in path: %s' % model_path)
    print('***End***')

