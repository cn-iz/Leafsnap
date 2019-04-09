import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import graph_util
from configparser import ConfigParser
import time
import cv2

# 生成tmp文件
with tf.Session(graph = tf.Graph()) as sess:
	sess.run(tf.global_variables_initializer())
	with gfile.FastGFile('./models/inception_dec_2015/tensorflow_inception_graph.pb', 'rb') as rf:
				graph_def = tf.GraphDef()
				graph_def.ParseFromString(rf.read())
				sess.graph.as_default()
				tf.import_graph_def(graph_def, name = '')
				# tf.summary.FileWriter('./tb', sess.graph)
	x1 = sess.graph.get_tensor_by_name('DecodeJpeg/contents:0')
	x2 = sess.graph.get_tensor_by_name('DecodeJpeg:0')
	y2048 = sess.graph.get_tensor_by_name('pool_3:0')
	def set_tmp(name):
		npar = []
		v_path = './datas/videos/%s' %name
		i_path = './datas/imgs/%s' %name
		print('开始提取%s'%name)
		# 预处理图片
		for fs in os.walk(i_path):
			for f in fs[2]:
				f_path = os.path.join(fs[0],f)
				image_data = gfile.FastGFile(f_path, 'rb').read()
				info = sess.run(y2048,feed_dict = {x1: image_data})
				info = np.squeeze(info)
				npar.append(info)
				# print(len(npar))
		# 预处理视频
		for vs in os.walk(v_path):
			for v in vs[2]:
				v_path = os.path.join(vs[0],v)
				video = cv2.VideoCapture()
				if not video.open(v_path):
					print("can not open the video")
					continue
				count = 0
				while True:
					_, frame = video.read()
					if frame is None:
						break
					# if count % 3  =  =  0:
					info = sess.run(y2048,feed_dict = {x2: frame})
					info = np.squeeze(info)
					npar.append(info)
					# print(len(npar))
					count += 1
				video.release()
		# print(len(npar))
		np.save('./datas/tmp/%s.npy'%name, np.array(npar))
		print('%s提取完成'%name)

	def init_tmp():
		columns = get_columns()
		for c in columns:
			set_tmp(c)

	# 扫描视频和图片返回类别
	def get_columns():
		print('开始扫描类别')
		columns = []
		for dir in os.listdir('./datas/imgs'):
			child = os.path.join('./datas/imgs', dir)
			if os.path.isdir(child):
				columns.append(dir)
		for dir in os.listdir('./datas/videos'):
			child = os.path.join('./datas/videos', dir)
			if os.path.isdir(child) and not dir in columns:
				columns.append(dir)
		print('扫描完成,共%s类'%len(columns))
		return columns

	# 加载numpy文件
	def loader_data():
		columns=[]
		datas=[]
		for c in os.listdir('./datas/tmp'):
			column = c.split('.')[0]
			columns.append(column)
		for c in columns:
			data=np.load('./datas/tmp/%s.npy'%c)
			datas.append(data)
		return columns,datas
	# init 表示是否重新生成.npy文件
	def get_data(init=False):
		if init:
			init_tmp()
		return loader_data()

	# get_data(True)
# columns,datas = get_data()
# train,test=to_train_test(datas)
# print(np.array(train))
# print(np.array(test))
# print(loader_data())
# print(get_columns())

