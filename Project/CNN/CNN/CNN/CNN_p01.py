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
outputNo = 8

phase = 1

#imgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01\\"
#imgsDir = "C:\\Users\\arsic\\Desktop\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\false_2020_06_10_10_00_57\\"
#imgsDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01\\"
imgsDir = "C:\\Users\\arsic\\Desktop\\1\\"
minMaxCSVpath = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
outputDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces_out\\"
drawOutputDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces_out_draw\\"

start = 0
max = 8000

images = []
filenames = []
minMaxValues = []
predictions = []

# debug
faceLocation = ''
faceLocationNorm = ''

def predictFace(vsource = 1, savePredictions = False):
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
            
            if(savePredictions):
                predictions.append(prediction)

            if(cv2.waitKey(25) & 0xFF == ord('q')):
                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,470)
                bottomLeftCornerOfText2 = (10,30)
                fontScale              = 0.5
                fontColor              = (0,0,255)
                lineType               = 2

                cv2.putText(frame,faceLocation, 
                            bottomLeftCornerOfText, 
                            font, 
                            fontScale,
                            fontColor,
                            lineType)
                cv2.putText(frame,faceLocationNorm, 
                            bottomLeftCornerOfText2, 
                            font, 
                            fontScale,
                            fontColor,
                            lineType)
                cv2.imwrite('C:\\Users\\Cisra\\Desktop\\face01.jpg', frame)

                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

# indexes + 1 because we added new expected prediction
def drawPredictionOnImage(prediction, image):
    global faceLocation
    global faceLocationNorm

    faceX = prediction[0][1]
    faceY = prediction[0][2]
    faceW = prediction[0][7]

    leftEyeX = prediction[0][3]
    leftEyeY = prediction[0][4]

    rightEyeX = prediction[0][5]
    rightEyeY = prediction[0][6]

    faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
    faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    #faceLocationNorm = "(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")"
    #faceLocation = "(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")"
    #print("(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")")
    #print("(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")")


    lEyeXDenom = (leftEyeX * (minMaxValues[1][2] - minMaxValues[0][2]) + minMaxValues[0][2])
    lEyeYDenom = (leftEyeY * (minMaxValues[1][3] - minMaxValues[0][3]) + minMaxValues[0][3])
    rEyeXDenom = (rightEyeX * (minMaxValues[1][4] - minMaxValues[0][4]) + minMaxValues[0][4])
    rEyeYDenom = (rightEyeY * (minMaxValues[1][5] - minMaxValues[0][5]) + minMaxValues[0][5])

    topLeftX = faceXDenom - int((faceWDenom / 2) + 0.5)
    topLeftY = faceYDenom - int(((faceWDenom / 2) * 1.5) + 0.5)

    bottomRightX = faceXDenom + int((faceWDenom / 2) + 0.5)
    bottomRightY = faceYDenom + int(((faceWDenom / 2) * 1.5) + 0.5)

    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
    cv2.rectangle(image, (int(lEyeXDenom),int(lEyeYDenom)), (int(lEyeXDenom + 3),int(lEyeYDenom + 3)) , (0,0,255), 2)
    cv2.rectangle(image, (int(rEyeXDenom),int(rEyeYDenom)), (int(rEyeXDenom + 3),int(rEyeYDenom + 3)) , (0,0,255), 2)

    #print("Face on: (" + str(prediction[0][1]) + ", " + str(prediction[0][2]) + ")")

    return image

def predictFromImages():

    global images
    global filenames
    global predictions

    [images, filenames] = Utilities.loadImagesAndGrayscale(imgsDir, images, inputWidth, inputHeight)

    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    predictions = model.predict(df_im, verbose = 1)

    # denormalize all predictions
    denormPredictions = denormalizeAllPredictions(predictions, minMaxValues)

    # first load images again because we at this point have only gray images
    images = []
    [images, filenames] = Utilities.loadImages(imgsDir, images)

    if path.exists(outputDir):
        shutil.rmtree(outputDir)
    if path.exists(drawOutputDir):
        shutil.rmtree(drawOutputDir)

    os.mkdir(outputDir)
    os.mkdir(drawOutputDir)

    # crop images
    cnt = 0    
    for img in images:
        # calculate coordinates to crop from

        if(denormPredictions[cnt][0] > 0.75):
            continue

        topLeftX = int(denormPredictions[cnt][1] - int((denormPredictions[cnt][7] / 2) + 0.5))
        topLeftY = int(denormPredictions[cnt][2] - int(((denormPredictions[cnt][7] / 2) * 1.5) + 0.5))

        bottomRightX = int(denormPredictions[cnt][1] + int((denormPredictions[cnt][7] / 2) + 0.5))
        bottomRightY = int(denormPredictions[cnt][2] + int(((denormPredictions[cnt][7] / 2) * 1.5) + 0.5))

        clippedValues = np.clip([topLeftX, topLeftY, bottomRightX, bottomRightY], a_min = 0, a_max = None)
        croppedImage = img[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]

        height = img.shape[0]
        width = img.shape[1]

        dimX = abs(bottomRightX - topLeftX)
        dimY = abs(bottomRightY - topLeftY)

        negX = 0
        negY = 0

        posX = 0
        posY = 0

        if(topLeftX < 0):
            negX = abs(topLeftX)
        if(topLeftY < 0):
            negY = abs(topLeftY)

        if(bottomRightX > width):
            posX = bottomRightX - width
        if(bottomRightY > height):
            posY = bottomRightY - height

        croppedImage = np.pad(croppedImage, ((negY, posY), (negX, posX), (0,0)), constant_values = 0)
        #img = drawPredictionOnImage([predictions[cnt]], img)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)
        cv2.imwrite(outputDir + filenames[cnt], croppedImage)

        tempImg = drawPredictionOnImage([predictions[cnt]], img)
        
        tempImg = cv2.cvtColor(tempImg, cv2.COLOR_BGR2RGB)
        cv2.imwrite(drawOutputDir + filenames[cnt], tempImg)

        cnt = cnt + 1


def denormalizeAllPredictions(predictions, minMaxValues):
    denormPredictions = predictions.copy()

    for pred in denormPredictions:
        pred[1] = int((pred[1] * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0]) + 0.5)
        pred[2] = int((pred[2] * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1]) + 0.5)
        pred[7] = int((pred[7] * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6]) + 0.5)

    return denormPredictions

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    model_name = "model_phase01.h5"
    model = cnn.create_model(inputWidth, inputHeight, 1, outputNo)

    model.load_weights(model_name)

    # load minimal and maximal values for denormalization
    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)

    # predict face from live video source
    #predictFace(1)

    # predict face from image source
    predictFromImages()

    Utilities.showStat(filenames, predictions, 1)
    Utilities.drawPredictionsToDisk(predictions, filenames, imgsDir, minMaxValues)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

