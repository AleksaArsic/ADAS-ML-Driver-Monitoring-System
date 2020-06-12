import numpy as np 
import pandas as pd 
import tensorflow as tf 
import Utilities
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import random
from time import time
import cv2

import os
from PIL import Image, ImageDraw
import PIL as PIL

import datetime

import CNNmodel as cnn

# data augumentation
# https://machinelearningmastery.com/how-to-configure-image-data-augmentation-when-training-deep-learning-neural-networks/
# shift left, right, top, down
# zoom in, zoom out


inputHeight = 100
inputWidth = 100
outputNo = 8

phase = 1

start = 0
max = 8000

imgsDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01\\"
normalizedDataPath = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized.csv"
minMaxCSVpath = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"

images=[]
categories = []
minMaxValues = []

r = 1

def plotTrainingResults(val_acc, val_loss, train_acc, train_loss):

    epochs = range(1,len(train_acc)+1)
    #Plottig the training and validation loss
    plt.plot(epochs, val_acc, 'bo', label='Validation Accuracy')
    plt.plot(epochs, train_acc, 'b', label='Train Accuracy')
    plt.title('Train and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('model_phase01.png')

    plt.clf()

    plt.plot(epochs, val_loss, 'r', label='Validation Loss')
    plt.plot(epochs, train_loss, 'b', label='Train Loss')
    plt.title('Loss / Mean Sqared Error')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('model_phase01_loss.png')

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)
    [images, categories, filenames] = Utilities.loadImagesAndCategories(images, imgsDir, categories, normalizedDataPath, phase = 1, inputWidth = inputWidth, inputHeight = inputHeight)

    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    # prebaci u format koji mrezi odgovara 
    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)
    df_cat = np.asarray(categories)
    df_cat = df_cat.reshape(df_cat.shape[0], outputNo)
    tr_im, val_im, tr_cat, val_cat = train_test_split(df_im, df_cat, test_size=0.2)


    #config = tf.compat.v1.ConfigProto()
    #config.gpu_options.allow_growth = True
    #session = tf.compat.v1.Session(config=config)


    tensorboard = TensorBoard(log_dir=imgsDir + "logs_img1" + "\{}".format(time()))

    model_name = "model_phase01.h5"
    callbacks = [
        EarlyStopping(monitor='val_accuracy', mode = 'max', patience=35, verbose=1),
        keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', mode = 'max', factor=0.5, patience=15, min_lr=0.000001, verbose=1),
        ModelCheckpoint(model_name, monitor='val_accuracy', mode = 'max', verbose=1, save_best_only=True, save_weights_only=True),
        tensorboard
    ]

    #network training
    model_history = model.fit(df_im, df_cat, # df_im - input ; df_cat - output
                    batch_size=2,
                    #batch_size=64,
                    epochs=350,
                    validation_data=(val_im, val_cat),
                    callbacks=callbacks,
                    verbose=1)

    #Visualizing accuracy and loss of training the model
    history_dict=model_history.history
    print(history_dict.keys())
    val_acc = history_dict['val_accuracy']
    val_loss = history_dict['val_loss']
    train_acc = history_dict['accuracy']
    train_loss = history_dict['loss']

    #plot accuracy and loss
    plotTrainingResults(val_acc, val_loss, train_acc, train_loss)

    script_end = datetime.datetime.now()
    print (script_end-script_start)
