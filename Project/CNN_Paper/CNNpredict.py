import cv2
import math
import random
import datetime
import glob, os
import Utilities
import PIL as PIL
import numpy as np 
import pandas as pd 
import CNNmodel as cnn
import tensorflow as tf 
from time import time
from tensorflow import keras
from PIL import Image, ImageDraw
import os.path
from os import path
import shutil

windowName = "Video source"

inputHeight = 100
inputWidth = 100
outputNo = 12

saveWidth = 200
saveHeight = 300

phase = 1

imgsDir = "D:\\ImageCapture\\ImageCapture\\output_2020_08_01_22_19_42\\"
minMaxCSVpath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
outputDir = "D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces_out\\"
drawOutputDir = "D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces_out_draw\\"

images = []
filenames = []
minMaxValues = []
predictions = []

def predictFromImages():

    global images
    global filenames
    global predictions

    [images, filenames] = Utilities.loadImagesAndGrayscale(imgsDir, images, inputWidth, inputHeight)

    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    predictions = model.predict(df_im, verbose = 1)

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    model_name = "model_paperCNN.h5"
    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    model.load_weights(model_name)

    # predict face from image source
    predictFromImages()

    Utilities.showStat(filenames, predictions, 1)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

