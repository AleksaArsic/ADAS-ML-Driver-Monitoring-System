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
outputNo = 15

phase = 3

#imgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase03\\"
imgsDir = "D:\\Diplomski_all\\final_test\\test_ph03\\"

images = []
filenames = []
predictions = []


if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    model_name = "model_phase03.h5"
    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    model.load_weights(model_name)

    # predict face from image source
    [images, filenames] = Utilities.loadImagesAndGrayscale(imgsDir, images, inputWidth, inputHeight)

    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    predictions = model.predict(df_im, verbose = 1)

    # write predictions to .csv file
    Utilities.showStat(filenames, predictions, 3)

    script_end = datetime.datetime.now()
    print (script_end-script_start)



