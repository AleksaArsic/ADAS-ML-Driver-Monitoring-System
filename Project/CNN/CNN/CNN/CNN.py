import numpy as np 
import pandas as pd 
import keras
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import random
from time import time
import cv2

import os
from PIL import Image, ImageDraw
import PIL as PIL

import tensorflow as tf 

import datetime
import glob, os

import CNNmodel as cnn

script_start = datetime.datetime.now()

lett_h = 100
lett_w = 100

imgs_dir = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\'

start = 0
max = 8000

r = 1

# Recreate the exact same model, including its weights and the optimizer

# Show the model architecture
model_name = "model_img"+str(r)+".h5"
#model = tf.keras.models.load_model(model_name)

model = cnn.create_model(lett_w, lett_h, 1)

#model = load_model(model_name)
model.load_weights(model_name)
model.summary()


def grayConversion(image):
    grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
    gray_img = grayValue.astype(np.uint8)
    return gray_img

def load_images(images):
    print ('loading  images  (' + str(start)+','+str(start+max)+ ')...')

    filenames = []

    os.chdir("D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\")
    for imagePath in glob.glob("*.jpg"):
        img = Image.open(imagePath)

        img = img.resize((lett_w,lett_h), Image.ANTIALIAS)
        img = np.asarray(img)
            
        gray = grayConversion(img)

        img1 = gray/255

        images.append(img1)
      
        fname = os.path.basename(imagePath)
        filenames.append(fname)

    print ('loading complete!')
    
    return [images, filenames]


images = []
filenames = []
[images, filenames] = load_images(images)

df_im = np.asarray(images)
df_im=df_im.reshape(df_im.shape[0], lett_w, lett_h, 1)

predictions = model.predict(df_im, verbose=0)

def drawPredictions(predictions, filenames):

    cnt = 0

    for fname in filenames:
        image_path='D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\' + fname

        faceX = predictions[cnt][0]
        faceY = predictions[cnt][1]
        faceW = predictions[cnt][6]

        #denormalize
        faceXDenom = (faceX * (457 - 192) + 192)
        faceYDenom = (faceY * (375 - 217) + 217)
        faceWDenom = (faceW * (304 - 128) + 128)

        img = Image.open(image_path)

        img = img.resize((lett_w,lett_h), Image.ANTIALIAS)
        img = np.asarray(img)
            
        gray = grayConversion(img)

        result = Image.fromarray((gray).astype(np.uint8))

        topLeftX = faceXDenom - (faceWDenom / 2)
        topLeftY = faceYDenom - ((faceWDenom / 2) * 1.5)

        topLeftX /= 6.4
        topLeftY /= 4.8

        bottomRightX = faceXDenom + (faceWDenom / 2)
        bottomRightY = faceYDenom + ((faceWDenom / 2) * 1.5)

        bottomRightX /= 6.4
        bottomRightY /= 4.8

        #draw rectangle on face
        test = ImageDraw.Draw(result)
        test.rectangle((topLeftX, topLeftX, 
                    bottomRightX, bottomRightY), outline = 'red')

        #result.show()
        result.save('D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\output_2020_04_17_11_39_49_grayscale_predictions\\' + fname)

        cnt = cnt + 1

def show_stat(filenames, predictions):
    cnt = 0
    ok_cnt = 0
    c1 = 0
    compare = []
    errors = []

    for fnames in filenames:
        f = filenames[cnt]
        c1 = 0
        ss = ''
        sctg = ''
        for item in predictions[cnt]:
            #if item>0.5:
            #    p=1
            #else:
            #    p=0
            p = item #predictions[cnt]
            predictions[cnt][c1] = p
            ss = ss+str(p)+','
            #c = categories[cnt][c1]
            #sctg = sctg+str(c)+','
            c1 = c1 + 1

        if ss==sctg:
            ok_cnt = ok_cnt + 1
        else:
            errors.append(f)

        s = f+','+ss

        compare.append(s)
        cnt = cnt+1

    with open('img' + str(r)+'_results_'+'_'+str(start)+'_'+str(start+max)+'.csv', 'w') as f:
        for item in compare:
            f.write("%s\n" % item)

    with open('Accuracy_img' + str(r)+'_results_'+'_'+str(start)+'_'+str(start+max)+'.csv', 'w') as f:
        f.write("Accuracy = %s\n" % str(ok_cnt/cnt))

    with open('errors.csv', 'w') as f:
        for item in errors:
            f.write("%s\n" % item)

show_stat(filenames, predictions)
drawPredictions(predictions, filenames)

script_end = datetime.datetime.now()
print (script_end-script_start)

