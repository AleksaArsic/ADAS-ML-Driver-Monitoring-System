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
faceOutputNo = 8
faceElementsOutputNo = 12

phase = 1

imgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01\\"
minMaxCSVpath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"

start = 0
max = 8000

images = []
filenames = []
minMaxValues = []
predictions = []

# debug
faceLocation = ''
faceLocationNorm = ''

def denormalizeFacePrediction(facePrediction):
    facePredictionDenorm = []

    faceX = facePrediction[0][1]
    faceY = facePrediction[0][2]
    faceW = facePrediction[0][7]

    #leftEyeX = prediction[0][3]
    #leftEyeY = prediction[0][4]

    #rightEyeX = prediction[0][5]
    #rightEyeY = prediction[0][6]

    faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
    faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    facePredictionDenorm.append(faceXDenom)
    facePredictionDenorm.append(faceYDenom)
    facePredictionDenorm.append(faceWDenom)
  
    return facePredictionDenorm

def denormalizeFaceElementsPrediction(faceElementsPrediction, faceWidth):

    predictions = faceElementsPrediction[0]

    for i in range(0, len(predictions), 2):
        predictions[i] *= faceWidth
        predictions[i + 1] *= (faceWidth * 1.5)
    
    return predictions

def cropFace(img, facePrediction):

    facePredictionDenormalized = denormalizeFacePrediction(facePrediction)

    topLeftX = int(facePredictionDenormalized[0] - math.ceil((facePredictionDenormalized[2] / 2)))
    topLeftY = int(facePredictionDenormalized[1] - math.ceil(((facePredictionDenormalized[2] / 2) * 1.5)))

    bottomRightX = int(facePredictionDenormalized[0] + math.ceil((facePredictionDenormalized[2] / 2)))
    bottomRightY = int(facePredictionDenormalized[1] + math.ceil(((facePredictionDenormalized[2] / 2) * 1.5)))

    croppedImage = img[topLeftY:bottomRightY, topLeftX:bottomRightX]
    #croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

    return croppedImage

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

    #debug
    #cv2.namedWindow("face")

    while(cap.isOpened()):  
        
        ret, frame = cap.read();
        
        if(ret == True):
            #grayFrame = Utilities.grayConversion(frame)
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #predict face
            img = cv2.resize(grayFrame, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            img1 = img/255

            facePrediction = face_model.predict(img1[np.newaxis, :, :, np.newaxis], verbose = 1)

            faceImg = cropFace(grayFrame, facePrediction)
            #cv2.imshow("face", faceImg)

            # predict face elements
            img = cv2.resize(faceImg, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            img1 = img/255

            faceElementsPrediction = face_elements_model.predict(img1[np.newaxis, :, :, np.newaxis], verbose = 1)

            # draw face bounding box and face elements on live stream
            drawPredictionOnImage(facePrediction, faceElementsPrediction, frame)
            cv2.imshow(windowName, frame)
            
            frameId += 1
            
            if(savePredictions):
                predictions.append(facePrediction)

            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def drawPredictionOnImage(facePrediction, faceElementsPrediction, image):
    #debug
    global faceLocation
    global faceLocationNorm

    faceElementsPredDenorm = []

    #faceX = facePrediction[0][1]
    #faceY = facePrediction[0][2]
    #faceW = facePrediction[0][7]

    #leftEyeX = faceElementsPrediction[0][2]
    #leftEyeY = faceElementsPrediction[0][3]

    #rightEyeX = faceElementsPrediction[0][4]
    #rightEyeY = faceElementsPrediction[0][5]

    faceXDenom = (facePrediction[0][1] * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
    faceYDenom = (facePrediction[0][2] * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceWDenom = (facePrediction[0][7] * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    #debug
    #faceLocationNorm = "(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")"
    #faceLocation = "(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")"
    #print("(x, y, w): (" + str(faceX) + ", " + str(faceY) + ", " + str(faceW) + ")")
    #print("(x, y, w): (" + str(faceXDenom) + ", " + str(faceYDenom) + ", " + str(faceWDenom) + ")")

    topLeftX = faceXDenom - int((faceWDenom / 2) + 0.5)
    topLeftY = faceYDenom - int(((faceWDenom / 2) * 1.5) + 0.5)

    bottomRightX = faceXDenom + int((faceWDenom / 2) + 0.5)
    bottomRightY = faceYDenom + int(((faceWDenom / 2) * 1.5) + 0.5)

    faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, faceWDenom)

    for i in range(0, len(faceElementsPredDenorm), 2):
        faceElementsPredDenorm[i] += topLeftX
        faceElementsPredDenorm[i + 1] += topLeftY

    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)), (0,255,0), 2)

    for i in range(0, len(faceElementsPredDenorm), 2):
        cv2.circle(image, (int(faceElementsPredDenorm[i]), int(faceElementsPredDenorm[i + 1])), 1, (0,255,0), 2)

    #print("Face on: (" + str(facePrediction[0][1]) + ", " + str(facePrediction[0][2]) + ")")

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

    # crop images

    cnt = 0    
    for img in images:
        # calculate coordinates to crop from

        topLeftX = int(denormPredictions[cnt][1] - int((denormPredictions[cnt][7] / 2)) + 0.5)
        topLeftY = int(denormPredictions[cnt][2] - int(((denormPredictions[cnt][7] / 2) * 1.5) + 0.5))

        bottomRightX = int(denormPredictions[cnt][1] + int((denormPredictions[cnt][7] / 2) + 0.5))
        bottomRightY = int(denormPredictions[cnt][2] + int(((denormPredictions[cnt][7] / 2) * 1.5) + 0.5))

        croppedImage = img[topLeftY:bottomRightY, topLeftX:bottomRightX]
        croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

        cv2.imwrite('D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces\\' + filenames[cnt] + '.jpg', croppedImage)

        cnt = cnt + 1


def denormalizeAllPredictions(predictions, minMaxValues):
    denormPredictions = predictions.copy()

    for pred in denormPredictions:
        pred[1] = (pred[1] * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
        pred[2] = (pred[2] * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
        pred[7] = (pred[7] * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    return denormPredictions

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # Recreate the exact same model
    face_model_name = "model_phase01.h5"
    face_elements_model_name = "model_phase02.h5"

    face_model = cnn.create_model(inputWidth, inputHeight, 1, faceOutputNo)
    face_elements_model = cnn.create_model(inputWidth, inputHeight, 1, faceElementsOutputNo)

    face_model.load_weights(face_model_name)
    face_elements_model.load_weights(face_elements_model_name)

    # load minimal and maximal values for denormalization
    minMaxValues = Utilities.readMinMaxFromCSV(minMaxCSVpath)

    # predict face from live video source
    predictFace(1)

    # predict face from image source
    #predictFromImages()

    #Utilities.showStat(filenames, predictions)
    #Utilities.drawPredictionsToDisk(predictions, filenames, imgsDir, minMaxValues)

    script_end = datetime.datetime.now()
    print (script_end-script_start)


