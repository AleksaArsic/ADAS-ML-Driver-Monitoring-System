import cv2
import math
import time
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
attentionOutputNo = 15

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

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

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

def denormalizeFaceElementsPrediction(faceElementsPrediction, elementWidth, start = 0, end = -1):

    predictions = faceElementsPrediction[0]

    if(end == -1):
        end = len(predictions)

    for i in range(start, end, 2):
        predictions[i] *= elementWidth
        predictions[i + 1] *= (elementWidth * 1.5)
    
    return predictions

def cropFace(img, facePrediction):

    facePredictionDenormalized = denormalizeFacePrediction(facePrediction)

    topLeftX = int(facePredictionDenormalized[0] - int((facePredictionDenormalized[2] / 2) + 0.5))
    topLeftY = int(facePredictionDenormalized[1] - int(((facePredictionDenormalized[2] / 2) * 1.5) + 0.5))

    bottomRightX = int(facePredictionDenormalized[0] + int((facePredictionDenormalized[2] / 2) + 0.5))
    bottomRightY = int(facePredictionDenormalized[1] + int(((facePredictionDenormalized[2] / 2) * 1.5) + 0.5))

    croppedImage = img[topLeftY:bottomRightY, topLeftX:bottomRightX]
    #croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

    return croppedImage

def cropEyes(faceImg, faceElementsPrediction):
    leftEye = []
    rightEye = []

    topLeft = (0, 0)
    topRight = (0, 0)

    if faceElementsPrediction[0][0] < 0.1:
        tl, br = cropPoints(faceElementsPrediction[0][2], faceElementsPrediction[0][3], faceImg)

        tlX, tlY = tl
        brX, brY = br

        leftEye = faceImg[tlY:brY, tlX:brX]
        topLeft = tl
    if faceElementsPrediction[0][1] < 0.1:
        tl, br = cropPoints(faceElementsPrediction[0][4], faceElementsPrediction[0][5], faceImg)
        tlX, tlY = tl
        brX, brY = br
        
        rightEye = faceImg[tlY:brY, tlX:brX]
        topRight = tl

    return [leftEye, rightEye, topLeft, topRight]

def cropPoints(x, y, faceImg):
    # calculate coordinates to crop from
    height, width = faceImg.shape

    tlEyeX = x - 0.15
    tlEyeY = y - 0.10
    brEyeX = x + 0.15
    brEyeY = y + 0.10

    tlEyeXdenorm = int((tlEyeX * width) + 0.5)
    tlEyeYdenorm = int((tlEyeY * (width * 1.5)) + 0.5)
    brEyeXdenorm = int((brEyeX * width) + 0.5)
    brEyeYdenorm = int((brEyeY * (width * 1.5)) + 0.5)

    return [(tlEyeXdenorm, tlEyeYdenorm), (brEyeXdenorm, brEyeYdenorm)]

def predictFace(vsource = 1, savePredictions = False):
    width = 0
    height = 0

    s_t, e_t = 0, 0

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
    #cv2.namedWindow("le")
    #cv2.namedWindow("re")

    while(cap.isOpened()):  
        s_time = time()

        ret, frame = cap.read()
        
        if(ret == True):

            #grayFrame = Utilities.grayConversion(frame)
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #predict face
            img = cv2.resize(grayFrame, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            img1 = img/255

            s_t = time()
            facePrediction = face_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()
            e_t = time()

            faceImg = cropFace(grayFrame, facePrediction)
            #cv2.imshow("face", faceImg)

            # predict face elements
            img = cv2.resize(faceImg, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            img1 = img/255

            faceElementsPrediction = face_elements_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()

            leftEyeImg, rightEyeImg, topELeft, topERight = cropEyes(faceImg, faceElementsPrediction)

            leftEyePrediction = []
            rightEyePrediction = []
            if len(leftEyeImg):
                img = cv2.resize(leftEyeImg, (inputWidth, inputHeight), Image.ANTIALIAS)
                img = np.asarray(img)
                img1 = img/255

                leftEyePrediction = attention_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()

            if len(rightEyeImg):
                img = cv2.resize(rightEyeImg, (inputWidth, inputHeight), Image.ANTIALIAS)
                img = np.asarray(img)
                img1 = img/255

                rightEyePrediction = attention_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()

            if len(leftEyePrediction):
                if(leftEyePrediction[0][0] < 0.5):
                    leftEyePrediction[0][0] = 0
                else:
                    leftEyePrediction[0][0] = 1

            if len(rightEyePrediction):
                if(rightEyePrediction[0][0] < 0.5):
                    rightEyePrediction[0][0] = 0
                else:
                    rightEyePrediction[0][0] = 1


            # draw face bounding box and face elements on live stream
            drawPredictionOnImage(facePrediction, faceElementsPrediction, frame, leftEyePrediction, rightEyePrediction, topELeft, topERight)
            cv2.imshow(windowName, frame)
            #cv2.imshow("le", leftEyeImg)
            #cv2.imshow("re", rightEyeImg)

            frameId += 1
            
            if(savePredictions):
                predictions.append(facePrediction)

            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break

        else:
            break

        e_time = time()
        elapsed = e_time - s_time
        el_time = e_t - s_t

        print("Processing time: " + str(el_time))
        print("Processing time of current frame: " + str(elapsed))
        print("FPS: " + str(1/elapsed))

    cap.release()
    cv2.destroyAllWindows()

def drawPredictionOnImage(facePrediction, faceElementsPrediction, image, leftEyePrediction, rightEyePrediction, topELeft, topERight):
    #debug
    global faceLocation
    global faceLocationNorm

    faceElementsPredDenorm = []
    leftEyePredDenorm = []
    rightEyePredDenorm = []

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

    leftEyePredDenorm = denormalizeFaceElementsPrediction(leftEyePrediction, faceWDenom * 0.3, 1, 11)
    rightEyePredDenorm = denormalizeFaceElementsPrediction(rightEyePrediction, faceWDenom * 0.3, 1, 11)

    #leftEyePredDenorm = denormalizeFaceElementsPrediction(leftEyePrediction, faceWDenom, 2, 11)

    #leftEyePredDenorm = denormalizeFaceElementsPrediction(leftEyePredDenorm, faceWDenom * 0.3)

    for i in range(0, len(faceElementsPredDenorm), 2):
        faceElementsPredDenorm[i] += topLeftX
        faceElementsPredDenorm[i + 1] += topLeftY

    for i in range(1, len(leftEyePredDenorm), 2):
        leftEyePredDenorm[i] += (faceElementsPredDenorm[0] + topELeft[0])
        leftEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topELeft[1])

    for i in range(1, len(rightEyePredDenorm), 2):
        rightEyePredDenorm[i] += (faceElementsPredDenorm[0] + topERight[0])
        rightEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topERight[1])

    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)), (0,255,0), 2)

    color = (0, 255, 0)

    if(leftEyePrediction[0][0] or rightEyePrediction[0][0]):
        color = (0, 0, 255)

    for i in range(1, len(leftEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(leftEyePredDenorm[i]), int(leftEyePredDenorm[i + 1])), 1, color, 2)

    for i in range(1, len(rightEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(rightEyePredDenorm[i]), int(rightEyePredDenorm[i + 1])), 1, color, 2)
    #for i in range(0, len(faceElementsPredDenorm), 2):
    #    cv2.circle(image, (int(faceElementsPredDenorm[i]), int(faceElementsPredDenorm[i + 1])), 1, color, 2)

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

    #my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    #tf.config.set_visible_devices([], 'GPU')

    # Recreate the exact same model
    face_model_name = "model_phase01.h5"
    face_elements_model_name = "model_phase02.h5"
    attention_model_name = "model_phase03.h5"

    face_model = cnn.create_model(inputWidth, inputHeight, 1, faceOutputNo)
    face_elements_model = cnn.create_model(inputWidth, inputHeight, 1, faceElementsOutputNo)
    attention_model = cnn.create_model(inputWidth, inputHeight, 1, attentionOutputNo)

    face_model.load_weights(face_model_name)
    face_elements_model.load_weights(face_elements_model_name)
    attention_model.load_weights(attention_model_name)

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

