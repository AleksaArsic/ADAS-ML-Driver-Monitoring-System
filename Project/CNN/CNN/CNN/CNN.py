import cv2
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

windowName = "Video source"

inputHeight = 100
inputWidth = 100

imgsDir = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\'
minMaxCSVpath = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49_faceMode_min_max.csv'
 
start = 0
max = 8000


def predictFace(vsource = 1):
    width = 0
    height = 0

    if(isinstance(vsource, int)):
        cap = cv2.VideoCapture(vsource + cv2.CAP_DSHOW)
        width  = cap.get(3)  # float
        height = cap.get(4) # float
        #change_res(cap, 1280, 720)
    else:
        cap = cv2.VideoCapture(vsource)

    if(cap.isOpened() == False):
        print("Error opening video source")

    # frame number
    frameId = 0

    cv2.namedWindow(windowName)

    while(cap.isOpened()):  
        
        ret, frame = cap.read();
        
        if(ret == True):
            #predict 
            img = cv2.resize(frame, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            gray = Utilities.grayConversion(img)
            img1 = gray/255

            prediction = model.predict(img1[np.newaxis, :, :, np.newaxis], verbose = 1)
            drawPredictionOnImage(prediction, frame)
            cv2.imshow(windowName, frame)
            
            frameId += 1
            
            if(cv2.waitKey(25) & 0xFF == ord('q')):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def drawPredictionOnImage(prediction, image):
        faceX = prediction[0][0]
        faceY = prediction[0][1]
        faceW = prediction[0][6]

        leftEyeX = prediction[0][2]
        leftEyeY = prediction[0][3]

        rightEyeX = prediction[0][4]
        rightEyeY = prediction[0][5]

        faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
        faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
        faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

        lEyeXDenom = (leftEyeX * (minMaxValues[1][2] - minMaxValues[0][2]) + minMaxValues[0][2])
        lEyeYDenom = (leftEyeY * (minMaxValues[1][3] - minMaxValues[0][3]) + minMaxValues[0][3])
        rEyeXDenom = (rightEyeX * (minMaxValues[1][4] - minMaxValues[0][4]) + minMaxValues[0][4])
        rEyeYDenom = (rightEyeY * (minMaxValues[1][5] - minMaxValues[0][4]) + minMaxValues[0][5])

        topLeftX = faceXDenom - (faceWDenom / 2)
        topLeftY = faceYDenom - ((faceWDenom / 2) * 1.5)

        bottomRightX = faceXDenom + (faceWDenom / 2)
        bottomRightY = faceYDenom + ((faceWDenom / 2) * 1.5)

        cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
        cv2.rectangle(image, (int(lEyeXDenom),int(lEyeYDenom)), (int(lEyeXDenom + 3),int(lEyeYDenom + 3)) , (0,0,255), 2)
        cv2.rectangle(image, (int(rEyeXDenom),int(rEyeYDenom)), (int(rEyeXDenom + 3),int(rEyeYDenom + 3)) , (0,0,255), 2)

        return image


if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    model_name = "model_img1.h5"
    model = cnn.create_model(inputWidth, inputHeight, 1)

    model.load_weights(model_name)

    # load minimal and maximal values for denormalization
    minMaxValues = []
    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)
    predictFace(1)

    #Utilities.showStat(filenames, predictions)
    #Utilities.drawPredictionsToDisk(predictions, filenames, imgsDir)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

