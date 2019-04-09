import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import graph_util
from configparser import ConfigParser
import time
import data_init

#全连接层输入尺寸
BOTTLENECK_TENSOR_SIZE = 2048

#训练类别数
N_CLASS= 6
LEARNING_RATE = 0.005
STEPS = 50
BATCH = 100

# 获取一批训练数据
def get_data_beach(datas):
	index=np.random.randint(len(datas),size=BATCH)
	x=[]
	y=[]
	for i in index:
		d=datas[i][random.randint(0,len(datas[i])-1)]
		x.append(d)
		ty=np.zeros(len(datas))
		ty[i]=1
		y.append(ty)
	return x,y
# 把数据分为测试集和训练集
def to_train_test(datas,rate=0.7):
	train=[]
	test={'x':[],'y':[]}
	for i in range(len(datas)):
		ds=[]
		for d in datas[i]:
			if random.random()<rate:
				ds.append(d)
			else:
				test['x'].append(d)
				ty=np.zeros(len(datas))
				ty[i]=1
				test['y'].append(ty)
		train.append(ds)
	return train,test

def model_save(sess, model_path, input_tensor_name, bottleneck_tensor_name):
    graph_def = tf.get_default_graph().as_graph_def()
    outpput_graph_def = graph_util.convert_variables_to_constants(sess, graph_def, [input_tensor_name, bottleneck_tensor_name])
    with tf.gfile.GFile(model_path, "wb") as wf:
        wf.write(outpput_graph_def.SerializeToString())
# 定义新模型
def inference(inputs):
    this_input = tf.reshape(inputs, [-1, BOTTLENECK_TENSOR_SIZE], name='input_images')
    weights = tf.get_variable("weights", [BOTTLENECK_TENSOR_SIZE, N_CLASS], initializer=tf.truncated_normal_initializer(stddev=0.001))
    biases = tf.get_variable("biases", [N_CLASS], initializer=tf.constant_initializer(0.0))
    logits = tf.add(tf.matmul(this_input, weights), biases, "logits")
    return logits

# 定义损失函数 交叉熵
def loss(logits, labels):
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels)
    return tf.reduce_mean(cross_entropy)

# 定义训练方法
def training(loss, learning_rate):
    tf.summary.scalar('loss', loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op
 
# 定义测试方法
def evaluation(logits, labels):
    with tf.name_scope('evaluation'):
        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
        evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return evaluation_step

def save_new_model(init=False):
	columns,datas=data_init.get_data(init)
	train,test=to_train_test(datas)
	global N_CLASS
	N_CLASS=len(columns)
	placeholder_input = tf.placeholder(tf.float32, [None, BOTTLENECK_TENSOR_SIZE], name='in_2048')
	placeholder_labels = tf.placeholder(tf.float32, [None, N_CLASS])

	logits = inference(placeholder_input)

	this_loss = loss(logits, placeholder_labels)

	train_step = training(this_loss, LEARNING_RATE)

	evaluation_step = evaluation(logits, placeholder_labels)

	init = tf.global_variables_initializer()
	with tf.Session() as sess:
		sess.run(init)
		for step in range(STEPS):
			x,y=get_data_beach(train)
			sess.run(train_step, feed_dict={placeholder_input:x,placeholder_labels:y})

			if step % 100 == 0 or step + 1 == STEPS:
				accuracy = sess.run(evaluation_step, feed_dict={placeholder_input:test['x'],placeholder_labels:test['y']})
				print("Step %d: Validation accuracy on random sampled %d examples = %.2f%%" % (step, BATCH, accuracy * 100))
		accuracy = sess.run(evaluation_step, feed_dict={placeholder_input:test['x'],placeholder_labels:test['y']})
		print("Final test accuracy = %.1f%%" % (accuracy * 100))
		model_save(sess,'./models/my_model/my_model.pb', "in_2048", 'logits')


save_new_model()
# save_to_merge()