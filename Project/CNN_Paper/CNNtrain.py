import numpy as np 
import pandas as pd 
import tensorflow as tf 
import Utilities
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from Utilities import trainTestDatasetSplit, writeTestToCsv, compareResults, denormalizePredictions

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
outputNo = 25

phase = 1

imgsDir = r"C:\Users\arsic\Desktop\master\Rad\output\\"
normalizedDataPath = r"C:\Users\arsic\Desktop\master\Rad\output_normalized.csv"
minMaxCSVpath = r"C:\Users\arsic\Desktop\master\Rad\minMaxOutput.csv"

images=[]
categories = []
testImages = [] 
testLabels = [] 

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

def determineLogicalFromPrediction(predictions):

    for i in range(len(predictions)):
        if(predictions[i] >= 0.5):
            predictions[i] = 1
        else:
            predictions[i] = 0

    return predictions

def calculateAccuracy(testLabels, predictions):
    accuracy = 0

    validSamples = 0
    invalidSamples = 0

    for i in range(len(testLabels)):
        if(testLabels[i] == predictions[i]):
            validSamples += 1
        else:
            invalidSamples += 1

    accuracy = validSamples / len(predictions)

    return accuracy

def compareEyeClosed(testLabels, predictions, predictionsAcc):

    # transpose elements
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    testLabels[3] = determineLogicalFromPrediction(testLabels[3])
    testLabels[14] = determineLogicalFromPrediction(testLabels[14])

    predictions[3] = determineLogicalFromPrediction(predictions[3])
    predictions[14] = determineLogicalFromPrediction(predictions[14])

    predictionsAcc[3] = calculateAccuracy(testLabels[3], predictions[3])
    predictionsAcc[14] = calculateAccuracy(testLabels[14], predictions[14])

    # transpose to normal
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    return predictionsAcc

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)
    [images, categories, filenames] = Utilities.loadImagesAndCategories(images, imgsDir, categories, normalizedDataPath, phase = 1, inputWidth = inputWidth, inputHeight = inputHeight)

    [testImages, testLabels] = trainTestDatasetSplit(images, categories)

    model_name = "model_paperCNN.h5"

    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    # change to cnn input format
    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)
    df_cat = np.asarray(categories)
    df_cat = df_cat.reshape(df_cat.shape[0], outputNo)
    tr_im, val_im, tr_cat, val_cat = train_test_split(df_im, df_cat, test_size=0.2)

    tensorboard = TensorBoard(log_dir=imgsDir + "logs_img1" + "\{}".format(time()))

    model_name = "model_paperCNN.h5"

    callbacks = [
        EarlyStopping(monitor='val_accuracy', mode = 'max', patience=50, verbose=1),
        keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', mode = 'max', factor=0.5, patience=15, min_lr=0.000001, verbose=1),
        ModelCheckpoint(model_name, monitor='val_accuracy', mode = 'max', verbose=1, save_best_only=True, save_weights_only=False),
        tensorboard
    ]


    #network training
    model_history = model.fit(df_im, df_cat, # df_im - input ; df_cat - output
                    batch_size=1,
                    #batch_size=64,
                    epochs=350,
                    validation_data=(val_im, val_cat),
                    callbacks=callbacks,
                    verbose=0)

    #Visualizing accuracy and loss of training the model
    history_dict=model_history.history
    print(history_dict.keys())
    val_acc = history_dict['val_accuracy']
    val_loss = history_dict['val_loss']
    train_acc = history_dict['accuracy']
    train_loss = history_dict['loss']

    #plot accuracy and loss
    plotTrainingResults(val_acc, val_loss, train_acc, train_loss)

    # predict on test dataset
    df_im = np.asarray(testImages)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    model = tf.keras.models.load_model(model_name)
    predictions = model.predict(df_im, verbose = 1)

    # denormalize test labels and predictions
    #denormalizePredictions(minMaxValues, testLabels)
    #denormalizePredictions(minMaxValues, predictions)

    # compare results between labeled test set and predictions
    testLabels = np.asarray(testLabels)
    predictionsAcc = compareResults(testLabels, predictions)

    #compareEyeClosed(testLabels, predictions, predictionsAcc)

    # write test results in .csv file
    writeTestToCsv(testLabels, predictions, predictionsAcc)

    script_end = datetime.datetime.now()
    print (script_end-script_start)
