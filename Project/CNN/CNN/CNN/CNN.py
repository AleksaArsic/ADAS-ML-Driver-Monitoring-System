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

windowName = "Video source"

inputHeight = 100
inputWidth = 100

imgsDir = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49\\'
minMaxCSVpath = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49_faceMode_min_max.csv'
 
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

def drawPredictionOnImage(prediction, image):
    global faceLocation
    global faceLocationNorm

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

    faceLocationNorm = "(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")"
    faceLocation = "(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")"
    print("(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")")
    print("(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")")


    lEyeXDenom = (leftEyeX * (minMaxValues[1][2] - minMaxValues[0][2]) + minMaxValues[0][2])
    lEyeYDenom = (leftEyeY * (minMaxValues[1][3] - minMaxValues[0][3]) + minMaxValues[0][3])
    rEyeXDenom = (rightEyeX * (minMaxValues[1][4] - minMaxValues[0][4]) + minMaxValues[0][4])
    rEyeYDenom = (rightEyeY * (minMaxValues[1][5] - minMaxValues[0][4]) + minMaxValues[0][5])

    topLeftX = faceXDenom - math.ceil((faceWDenom / 2))
    topLeftY = faceYDenom - math.ceil(((faceWDenom / 2) * 1.5))

    bottomRightX = faceXDenom + math.ceil((faceWDenom / 2))
    bottomRightY = faceYDenom + math.ceil(((faceWDenom / 2) * 1.5))

    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
    cv2.rectangle(image, (int(lEyeXDenom),int(lEyeYDenom)), (int(lEyeXDenom + 3),int(lEyeYDenom + 3)) , (0,0,255), 2)
    cv2.rectangle(image, (int(rEyeXDenom),int(rEyeYDenom)), (int(rEyeXDenom + 3),int(rEyeYDenom + 3)) , (0,0,255), 2)

    print("Face on: (" + str(prediction[0][0]) + ", " + str(prediction[0][1]) + ")")

    return image

def predictFromImages():

    global images
    global filenames

    [images, filenames] = Utilities.loadImagesAndGrayscale(imgsDir, images, inputWidth, inputHeight)

    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    predictions = model.predict(df_im, verbose = 1)

    # denormalize all predictions
    denormalizeAllPredictions(predictions, minMaxValues)

    # first load images again because we at this point have only gray images
    images = []
    [images, filenames] = Utilities.loadImages(imgsDir, images)

    # crop images

    cnt = 0    
    for img in images:
        # calculate coordinates to crop from

        topLeftX = int(predictions[cnt][0] - math.ceil((predictions[cnt][6] / 2)))
        topLeftY = int(predictions[cnt][1] - math.ceil(((predictions[cnt][6] / 2) * 1.5)))

        bottomRightX = int(predictions[cnt][0] + math.ceil((predictions[cnt][6] / 2)))
        bottomRightY = int(predictions[cnt][1] + math.ceil(((predictions[cnt][6] / 2) * 1.5)))

        croppedImage = img[topLeftY:bottomRightY, topLeftX:bottomRightX]
        croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

        cv2.imwrite('D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\output_2020_04_17_11_39_49_faces\\' + filenames[cnt] + '.jpg', croppedImage)

        cnt = cnt + 1


def denormalizeAllPredictions(predictions, minMaxValues):

    for pred in predictions:
        pred[0] = (pred[0] * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
        pred[1] = (pred[1] * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
        pred[6] = (pred[6] * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])


if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    model_name = "model_img1.h5"
    model = cnn.create_model(inputWidth, inputHeight, 1)

    model.load_weights(model_name)

    # load minimal and maximal values for denormalization
    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)

    # predict face from live video source
    predictFace(1)

    # predict face from image source
    #predictFromImages()

    #Utilities.showStat(filenames, predictions)
    #Utilities.drawPredictionsToDisk(predictions, filenames, imgsDir)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

