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

testImgsDir = r"D:\Diplomski_all\final_test\test_ph01"
testNormalizedDataPath = r"D:\Diplomski_all\final_test\test_ph01\expected.csv"
testMinMaxCSVpath = r"D:\Diplomski\DriverMonitoringSystem\Dataset\trainingSet_phase01_csv\trainingSet_phase01_normalized_min_max.csv"


images=[]
categories = []
testImages = [] 
testLabels = [] 

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # load test dataset
    [testImages, testLabels, filenames] = Utilities.loadImagesAndCategories(testImages, testImgsDir, testLabels, testNormalizedDataPath, phase = 1, inputWidth = inputWidth, inputHeight = inputHeight)

    model_name = "model_phase01.h5"

    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    # change to cnn input format
    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)
    df_cat = np.asarray(categories)
    df_cat = df_cat.reshape(df_cat.shape[0], outputNo)
    tr_im, val_im, tr_cat, val_cat = train_test_split(df_im, df_cat, test_size=0.2)

    model = tf.keras.models.load_model(model_name)
    predictions = model.predict(df_im, verbose = 1)

    # denormalize test labels and predictions
    denormalizePredictions(minMaxValues, testLabels)
    denormalizePredictions(minMaxValues, predictions)

    # compare results between labeled test set and predictions
    testLabels = np.asarray(testLabels)
    predictionsAcc = compareResults(testLabels, predictions)

    # write test results in .csv file
    writeTestToCsv(testLabels, predictions, predictionsAcc)

    script_end = datetime.datetime.now()
    print (script_end-script_start)
