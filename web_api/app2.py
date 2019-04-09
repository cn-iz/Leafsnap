from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

import glob
import os.path
import random
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import graph_util

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

from PIL import Image
import logging
import time
import datetime
from flask import make_response, jsonify
import cv2


# Define a flask app
app = Flask(__name__,static_folder='/static')

clas=["枫叶","桂花","银杏","五味子","杨梅","柳杉"]

with tf.Session(graph=tf.Graph()) as sess:
    sess.run(tf.global_variables_initializer())

    tf.saved_model.loader.load(sess, ["serve"], "./model/modelbase")
    graph = tf.get_default_graph()
    x = sess.graph.get_tensor_by_name('my_input:0')
    y = sess.graph.get_tensor_by_name('my_output:0')
    x2 = sess.graph.get_tensor_by_name('import/DecodeJpeg:0')

    def model_predict(img):
        # image_data = gfile.FastGFile(img, 'rb').read()
        r=sess.run(y,
               feed_dict={x2:img })
        # app.logger.info("图片预测完成")
        return r
    def model_predict1(img):
        image_data = gfile.FastGFile(img, 'rb').read()
        r=sess.run(y,
               feed_dict={x:image_data })
        return r

    @app.route('/predict', methods=['GET', 'POST'])
    def upload():
        # return request.method
        if request.method == 'POST':
            f = request.files['img']
            # app.logger.info("图片接收完成")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            t = time.time()
            f_name=str(int(t))+str(random.randint(1000 , 9999))+'.'+f.filename.rsplit('.',1)[1]
            upload_path = os.path.join(basepath, 'data/up_images',f_name)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            preds = model_predict1(upload_path)
            res=[i for i in preds[0]]
            return str(res)
        return "get"

    @app.route('/predict_video', methods=['GET', 'POST'])
    def predict_video():
        if request.method == 'POST':
            f = request.files['video']
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            t = time.time()
            na=str(int(t))+str(random.randint(1000 , 9999))
            f_name=na+'.'+f.filename.rsplit('.',1)[1]
            upload_path = os.path.join(basepath, 'data','up_videos',f_name)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            res=get_pictures(upload_path,na)
            # print(res)
            index=1
            r=np.array([0,0,0,0,0,0])
            for re in res:
                r=r+model_predict(re)[0]
            r2=[i/len(res) for i in r]
            return str(r2)
        return "get"
    def get_pictures(path,f_name):
        video = cv2.VideoCapture()
        if not video.open(path):
            print("can not open the video")
            return []
        count=video.get(cv2.CAP_PROP_FRAME_COUNT)
        flags=random.sample(range(0,int(count)-1),4)
        pcs=[]
        for flag in flags:
            video.set(cv2.CAP_PROP_POS_FRAMES,flag) #设置帧数标记
            ret,im = video.read()#获取图像
            pcs.append(im)
        video.release()
        return pcs

    @app.route('/html', methods=['GET'])
    def html():
        return '<!DOCTYPE html><html><head><title></title></head><body><form action="/predict_video" method="post" enctype="multipart/form-data"><input type="file" name="video" ><input type="submit" value="Submit"></form> </body></html>'


    if __name__ == '__main__':
    #     # app.debug = True
    #     # app.run(port=5000)
        app.debug = True
        app.run()
# video = cv2.VideoCapture()
# if not video.open('D:\\GraduationProject\\web_api\\data\\up_videos\\15527512996538.mp4'):
#     print("can not open the video")
# print(video.get(cv2.CAP_PROP_FRAME_COUNT))

