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
outputNo = 15 #ph1: 12 ph2: 16 ph3: 15

phase = 3

modelPath_ph01 = r"c:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Project\driverMonitoringSystem\driverMonitoringSystem\\model_phase01.h5"
modelPath_ph02 = r"c:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Project\driverMonitoringSystem\driverMonitoringSystem\\model_phase02.h5"
modelPath_ph03 = r"c:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Project\driverMonitoringSystem\driverMonitoringSystem\\model_phase03.h5"

testImgsDir = r"c:\Users\arsic\Desktop\master\Rad\final_test\test_ph03\\"
testNormalizedDataPath = r"c:\Users\arsic\Desktop\master\Rad\final_test\test_ph03\expected_norm.csv"
testMinMaxCSVpath = r"D:\Diplomski\DriverMonitoringSystem\Dataset\trainingSet_phase03_csv\trainingSet_phase03_normalized_min_max.csv"

testImages = [] 
testLabels = [] 

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

def compareLogical(testLabels, predictions, predictionsAcc, ph = 1):

    start = 0
    end = 0

    if(ph == 1):
        start = 7
        end = 11
    elif(ph == 2):
        start = 12 
        end = 16
    else:
        start = 11
        end = 15

    # transpose elements
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    testLabels[0] = determineLogicalFromPrediction(testLabels[0])
    predictions[0] = determineLogicalFromPrediction(predictions[0])
    predictionsAcc[0] = calculateAccuracy(testLabels[0], predictions[0])

    if(ph == 2):
        testLabels[1] = determineLogicalFromPrediction(testLabels[1])
        predictions[1] = determineLogicalFromPrediction(predictions[1])
        predictionsAcc[1] = calculateAccuracy(testLabels[1], predictions[1])       

    for i in range(start, end):
        testLabels[i] = determineLogicalFromPrediction(testLabels[i])
        predictions[i] = determineLogicalFromPrediction(predictions[i])
        predictionsAcc[i] = calculateAccuracy(testLabels[i], predictions[i])

    # transpose to normal
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    return predictionsAcc

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # load test dataset
    [testImages, testLabels, filenames] = Utilities.loadImagesAndCategories(testImages, testImgsDir, testLabels, testNormalizedDataPath, phase, inputWidth = inputWidth, inputHeight = inputHeight)

    # change to cnn input format
    df_im = np.asarray(testImages)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)
    df_cat = np.asarray(testLabels)
    df_cat = df_cat.reshape(df_cat.shape[0], outputNo)

    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    if(phase == 1):
        model = tf.keras.models.load_model(modelPath_ph01)
    if(phase == 2):
        model = tf.keras.models.load_model(modelPath_ph02)
    if(phase == 3):
        model = tf.keras.models.load_model(modelPath_ph03)

    predictions = model.predict(df_im, verbose = 1)

    # denormalize test labels and predictions
    #denormalizePredictions(minMaxValues, testLabels)
    #denormalizePredictions(minMaxValues, predictions)

    # compare results between labeled test set and predictions
    testLabels = np.asarray(testLabels)
    predictionsAcc = compareResults(testLabels, predictions)

    compareLogical(testLabels, predictions, predictionsAcc, phase)

    # write test results in .csv file
    writeTestToCsv(testLabels, predictions, predictionsAcc)

    script_end = datetime.datetime.now()
    print (script_end-script_start)
