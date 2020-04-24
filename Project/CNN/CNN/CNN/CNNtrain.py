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

import CNNmodel as cnn

script_start = datetime.datetime.now()

# data augumentation
# https://machinelearningmastery.com/how-to-configure-image-data-augmentation-when-training-deep-learning-neural-networks/
# shift left, right, top, down
# zoom in, zoom out

lett_h = 100
lett_w = 100

def read_data (idx):
    result = []
    dat_file = open('D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\4_norm2.csv','r')
    lines=dat_file.readlines()
    for line in lines:
        if len(line)>0:
            p1 = line.find(',')
            filename = line[0:p1]
            categ = line[p1+1:]
            s = filename+','+categ
            result.append(s)
    return result

imgs_dir = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\'

start = 0
max = 8000

r = 1

def drawExpected(grayImg, fname, faceX, faceY, faceW):
    #denormalize
    faceXDenom = (faceX * (455 - 192) + 192)
    faceYDenom = (faceY * (373 - 215) + 215)
    faceWDenom = (faceW * (304 - 128) + 128)

    result = Image.fromarray((grayImg).astype(np.uint8))

    topLeftX = faceXDenom - (faceWDenom / 2)
    topLeftY = faceYDenom - ((faceWDenom / 2) * 1.5)

    topLeftX /= 6.4
    topLeftY /= 4.8

    bottomRightX = faceXDenom + (faceWDenom / 2)
    bottomRightY = faceYDenom + ((faceWDenom / 2) * 1.5)

    bottomRightX /= 6.4
    bottomRightY /= 4.8

    #draw rectangle on face
    cv2.rectangle(grayImg, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
    cv2.imwrite('output_2020_04_17_11_39_49_grayscale\\' + fname + '.jpg', grayImg)



def grayConversion(image):
    grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
    gray_img = grayValue.astype(np.uint8)
    return gray_img

def load_images(images, categories):
    print ('loading  images  (' + str(start)+','+str(start+max)+ ')...')

    filenames = []
    lines = read_data (r)
    cnt = 0
    for line in lines:
        #if len(line)>0:

        if cnt < 2:
           cnt = cnt + 1
           continue

        faceX = 0
        faceY = 0
        faceW = 0

        if (len(line)>0) & (cnt>=start) & (cnt <= (start + max)):
            p1 = line.find(',')
            fname = line[0:p1]
            p1 = p1+1
            image_path='D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\' + fname + '.jpg'
            filenames.append(fname)

            cat=line[p1:]

            cat = cat.rstrip(',\n')
            cat = cat.split(',')
            cat.pop(6)
            cat.pop(6)
            cat.pop(6)
            cat.pop(6)

            cnt = 0
            for item in cat:
                cat[cnt] = float(item)
                cnt = cnt + 1
            cat = np.asarray(cat)

            faceX = cat[0]
            faceY = cat[1]
            faceW = cat[6]

            categories.append(cat)

            img = Image.open(image_path)

            img = img.resize((lett_w,lett_h), Image.ANTIALIAS)
            img = np.asarray(img)
            
            gray = grayConversion(img)

            # debug
            drawExpected(gray, fname, faceX, faceY, faceW)
            
            img1 = gray/255

            images.append(img1)

        cnt = cnt + 1
    print ('loading complete!')
    
    return [images, categories, filenames]

images=[]
categories = []

[images, categories, filenames] = load_images(images, categories)

model = cnn.create_model(lett_w, lett_h, 1)

# prebaci u format koji mrezi odgovara 
df_im = np.asarray(images)
df_im=df_im.reshape(df_im.shape[0], lett_w, lett_h, 1)
df_cat = np.asarray(categories)
df_cat = df_cat.reshape(df_cat.shape[0], 7)
tr_im, val_im, tr_cat, val_cat = train_test_split(df_im, df_cat, test_size=0.2)


config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

tensorboard = TensorBoard(log_dir=imgs_dir + "logs_img" + str(r) + "\{}".format(time()))

model_name = "model_img"+str(r)+".h5"
callbacks = [
    EarlyStopping(monitor='val_accuracy', mode = 'max', patience=350, verbose=1),
    keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', mode = 'max', factor=0.25, patience=15, min_lr=0.000001, verbose=1),
    ModelCheckpoint(model_name, monitor='val_accuracy', mode = 'max', verbose=1, save_best_only=True, save_weights_only=True),
    tensorboard
]

#network training
model_history = model.fit(df_im, df_cat, # df_im - input ; df_cat - output
            batch_size=2,
            #batch_size=64,
            epochs=350,
            validation_data=(val_im, val_cat),
            callbacks=callbacks
)

model.load_weights(model_name)


#Visualizing accuracy and loss of training the model
history_dict=model_history.history
print(history_dict.keys())
train_acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']


epochs = range(1,len(train_acc)+1)
#Plottig the training and validation loss
plt.plot(epochs, val_acc, 'bo', label='Validation Accuracy')
plt.plot(epochs, train_acc, 'b', label='Train Accuracy')
plt.title('Train and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('model'+str(r)+'_'+str(start)+'_'+str(start+max)+'.png')


script_end = datetime.datetime.now()
print (script_end-script_start)
