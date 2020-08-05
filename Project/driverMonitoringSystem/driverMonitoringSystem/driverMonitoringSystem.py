import cv2
import math
import time
import random
import datetime
import glob, os
import PIL as PIL
import numpy as np 
import pandas as pd 
import CNNmodel as cnn
import tensorflow as tf 
from time import time
from time import clock, sleep
from tensorflow import keras
from PIL import Image, ImageDraw, ImageFont
import winsound
import threading

# window names
mainWindowName = "Video source"
faceWindowName = "Face tracking"
eyeWindowName = "eye tracking"

# video source
vSource = 0

# path to .csv files with minimal and maximal values used for denormalization
minMaxCSVpath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
minMaxPhase02 = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase02_csv\\trainingSet_phase02_normalized_min_max.csv"
minMaxPhase03 = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase03_csv\\trainingSet_phase03_normalized_min_max.csv"

# path to .csv files with minimal and maximal values used for denormalization
#minMaxCSVpath = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
#minMaxPhase02 = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\Dataset\\trainingSet_phase02_csv\\trainingSet_phase02_normalized_min_max.csv"
#minMaxPhase03 = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\Dataset\\trainingSet_phase03_csv\\trainingSet_phase03_normalized_min_max.csv"

# minimal and maximal values arrays needed for data denormalization
minMaxValuesPh01 = []
minMaxValuesPh02 = []
minMaxValuesPh03 = []

# neural network input specifics
inputHeight = 100
inputWidth = 100
faceOutputNo = 8
faceElementsOutputNo = 16
attentionOutputNo = 15

# application FPS counter
currentFPS = 0

########## CONSTANTS ##########

# opencv width and height information index
cCVwidth = 3
cCVheight = 4

# constant resolution values
cResolutionWidth = 640
cResolutionHeight = 480

# minimal and maximal index in minMaxValuesPh0x
cMin = 0
cMax = 1

# indexes of face points of interest in face prediction array
cNoFace = 0 
cFaceX = 1
cFaceY = 2
cFaceW = 11
cFaceWminMax = 7

# start indexes of Face angle fields in prediction array
cFaceAngleStartIndex = 7
cFaceAngleEndIndex = 11

# indexes of face point of interest in denormalized face prediction array
cFaceXdenorm = 0
cFaceYdenorm = 1
cFaceWdenorm = 2

# indexes of eyes data in face elements prediction array
cNoLeftEye = 0
cNoRightEye = 1
cLeftEyeX = 2
cLeftEyeY = 3
cRightEyeX = 4
cRightEyeY = 5

# indexes of eyes in eyesData array
cEyesDataLeft = 0
cEyesDataRight = -1

# indexes of eyes data in attention prediction array (eyesPrediction)
cEyeClosed = 0
cPupilsStartIndex = 11

# constant ratio of face to width (2:3)
cFaceWidthHeightRatio = 1.5
# constant eye width in percentage
cEyeWidthPerc = 0.3
# constant eye height in percentage
cEyeHeightPerc = 0.2

# constant face height in labeled trainingSet_phase02
# phase02 neural network model outputs data for 200x300 constant face sizes scaled down to 100x100
# this value is needed for denormalization to calculate resize factor when tracking 
# points of interest on original image
cLabeledFaceHeight = 300

### THRESHOLDS ###
cNoFaceThreshold = 0.5 #(1 is debug value)
cFaceHasAngle = 0.5
cNoEyeThreshold = 0.5
cEyeOpenThreshold = 0.5
cEyePupilDirectionThreshold = 0.5

# constant integer true/false values
cTrue = 1
cFalse = 0

# on how many fps to average predictions
cAverageFps = 2

### INFO CONSTANTS ###

# information font color
infoFontColor = (0, 0, 0, 0)
# driver not present font color
driverFontColor = (0, 0, 255, 0)

cInfoDY = 20
cInfoX = 15
cDriverInfoX = 140
cDriverInfoY = 250

### MOVING AVERAGE WINDOW SIZE ###
cFaceWindowSize = 15
cFaceElementsWindowSize = 15
cEyesWindowSize = 10

### ATTENTION LOGIC ###
# time interval for attention check in seconds
cTimeInterval = 2.5

# holidng eyes predictions for both eyes
eyesAttentionList = [[], []]

# holding face predictions
faceAttentionList = []

# index of left and right eye data in eyesAttentionList
cLeftEyeAtt = 0
cRightEyeAtt = 1

# sound duration in ms
cSoundDuration = 1000
# sound frequency
cSoundFrequency = 1000

# EYES CLOSED THRESHOLD 
# if sum of 'eyeClosed' predictions for both eyes are greater than this number
# give a sound warning
cEyesClosedThreshold = 35

# FACE HAS ANGLE THRESHOLD
# if there is more than cFaceHasAngleThreshold predictions in face prediction array 
# that have an angle fields set to 1 give a sound warning
cFaceHasAngleThreshold = 40 

###############################

# set desired resolution for video source
# this function does not check if the desired resolution is supported by the device
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# used for reading whole .csv files
def readCSV(filepath):
    result = []
    datFile = open(filepath,'r')
    lines=datFile.readlines()
    for line in lines:
        if len(line)>0:
            p1 = line.find(',')
            filename = line[0:p1]
            categ = line[p1+1:]
            s = filename+','+categ
            result.append(s)
    return result

# used for parsing .csv files with minimal and maximal values
# used for normalization and denormalization
def readMinMaxFromCSV(filepath):
	
	lines = readCSV(filepath)
	cnt = 0
	result = []
	
	for line in lines:
		
		if(cnt < 2):
			cnt = cnt + 1
			continue
		
		if(len(line) > 0):
			p1 = line.find(',')
			p1 = p1+1
			cat=line[p1:]

			cat = cat.rstrip(',\n')
			cat = cat.split(',')
			
			cntCat = 0
			for item in cat:
				cat[cntCat] = float(item)
				cntCat = cntCat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result

# denormalize face predictions from normalized range (0, 1) to pixel values of the original image
# does not change original prediction array
def denormalizeFacePrediction(facePrediction):
    facePredictionDenorm = []

    faceXDenom = (facePrediction[0][cFaceX] * (minMaxValuesPh01[cMax][cFaceX - 1] - minMaxValuesPh01[cMin][cFaceX - 1]) + minMaxValuesPh01[cMin][cFaceX - 1])
    faceYDenom = (facePrediction[0][cFaceY] * (minMaxValuesPh01[cMax][cFaceY - 1] - minMaxValuesPh01[cMin][cFaceY - 1]) + minMaxValuesPh01[cMin][cFaceY - 1])
    faceWDenom = (facePrediction[0][cFaceW] * (minMaxValuesPh01[cMax][cFaceWminMax - 1] - minMaxValuesPh01[cMin][cFaceWminMax - 1]) + minMaxValuesPh01[cMin][cFaceWminMax - 1])

    facePredictionDenorm.append(faceXDenom)
    facePredictionDenorm.append(faceYDenom)
    facePredictionDenorm.append(faceWDenom)
  
    return facePredictionDenorm

# denormalize face elements predictions from normalized range (0, 1) to pixel values of the face image
# changes are made directly to original prediction array
def denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor):

    faceElementsPredDenorm = []

    faceElementsPredDenorm.append(faceElementsPrediction[0][0])
    faceElementsPredDenorm.append(faceElementsPrediction[0][1])

    for i in range(2, len(faceElementsPrediction[0]) - 4):
        faceElementsPredDenorm.append(int(((faceElementsPrediction[0][i] * (minMaxValuesPh02[1][i - 2] - minMaxValuesPh02[0][i - 2]) + minMaxValuesPh02[0][i - 2]) / resizeFactor) + 0.5))

    return [faceElementsPredDenorm]

# denormalize eyes prediction
# does not change original prediction array
def denormalizeEyesPrediction(faceElementsPrediction, elementWidth, start = 0, end = -1):

    predictions = faceElementsPrediction.copy()

    if(end == -1):
        end = len(predictions)

    widthFactor = (inputWidth / elementWidth)
    heightFactor = (inputHeight / (elementWidth / cEyeWidthPerc * cFaceWidthHeightRatio * cEyeHeightPerc))

    for i in range(start, end):
        if(i % 2 == 0):
            resizeFactor = heightFactor
        else:
            resizeFactor = widthFactor

        predictions[i] = int(((predictions[i] * (minMaxValuesPh03[cMax][i - 1] - minMaxValuesPh03[cMin][i - 1]) + minMaxValuesPh03[cMin][i - 1]) / resizeFactor) + 0.5)
    
    return predictions

# crops face image from original image
def cropFace(img, facePrediction):

    facePredictionDenormalized = denormalizeFacePrediction(facePrediction)

    topLeftX = int(facePredictionDenormalized[cFaceXdenorm] - int((facePredictionDenormalized[cFaceWdenorm] / 2) + 0.5))
    topLeftY = int(facePredictionDenormalized[cFaceYdenorm] - int(((facePredictionDenormalized[cFaceWdenorm] / 2) * cFaceWidthHeightRatio) + 0.5))

    bottomRightX = int(facePredictionDenormalized[cFaceXdenorm] + int((facePredictionDenormalized[cFaceWdenorm] / 2) + 0.5))
    bottomRightY = int(facePredictionDenormalized[cFaceYdenorm] + int(((facePredictionDenormalized[cFaceWdenorm] / 2) * cFaceWidthHeightRatio) + 0.5))

    faceCoords = [topLeftX, topLeftY, bottomRightX, bottomRightY]
    clippedValues = np.clip([topLeftX, topLeftY, bottomRightX, bottomRightY], a_min = 0, a_max = None)

    croppedImage = img[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]
    croppedImage = addFacePadding(croppedImage, faceCoords, img.shape)

    return croppedImage

# adds padding to face image if it's not in ratio 3:2
def addFacePadding(img, faceCoords = [], fullImgDim = (0,0)):
    croppedImage = []

    height, width = fullImgDim
    dimX = abs(faceCoords[2] - faceCoords[0])
    dimY = abs(faceCoords[3] - faceCoords[1])

    negX = 0
    negY = 0

    posX = 0
    posY = 0

    if(faceCoords[0] < 0):
        negX = abs(faceCoords[0])
    if(faceCoords[1] < 0):
        negY = abs(faceCoords[1])

    if(faceCoords[2] > width):
        posX = faceCoords[2] - width
    if(faceCoords[3] > height):
        posY = faceCoords[3] - height

    croppedImage = np.pad(img, ((negY, posY), (negX, posX)), constant_values = 0)

    return croppedImage

# crops eyes from face image
def cropEyes(faceImg, faceElementsPrediction):
    leftEye = []
    rightEye = []

    resizeFactor = cLabeledFaceHeight / faceImg.shape[0]

    faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor)

    if faceElementsPrediction[0][cNoLeftEye] < cNoEyeThreshold:
        tl, br = eyeCropPoints(faceElementsPredDenorm[0][cLeftEyeX], faceElementsPredDenorm[0][cLeftEyeY], faceImg)

        clippedValues = np.clip([int(tl[0]), int(tl[1]), int(br[0]), int(br[1])], a_min = 0, a_max = None)
        leftEye = faceImg[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]
    
    if faceElementsPrediction[0][cNoRightEye] < cNoEyeThreshold:
        tl, br = eyeCropPoints(faceElementsPredDenorm[0][cRightEyeX], faceElementsPredDenorm[0][cRightEyeY], faceImg)
        
        clippedValues = np.clip([int(tl[0]), int(tl[1]), int(br[0]), int(br[1])], a_min = 0, a_max = None)
        rightEye = faceImg[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]

    return [leftEye, rightEye]

def eyeCropPoints(x, y, faceImg):
    # calculate coordinates to crop from
    height, width = faceImg.shape
    
    tlEyeX = x - int(cEyeWidthPerc / 2 * width)
    tlEyeY = y - int(cEyeHeightPerc / 2 * height)
    brEyeX = x + int(cEyeWidthPerc / 2 * width)
    brEyeY = y + int(cEyeHeightPerc / 2 * height)

    return [(tlEyeX, tlEyeY), (brEyeX, brEyeY)]

# check if 'eyeClosed' is above cEyeOpenThreshold and set it to 1 if above
def correctEyesPrediction(eyePrediction = []):
    # left and right eye open prediction correct
    if len(eyePrediction):
        if(eyePrediction[cEyeClosed] < cEyeOpenThreshold):
            eyePrediction[cEyeClosed] = cFalse
        else:
            eyePrediction[cEyeClosed] = cTrue

        for i in range(cPupilsStartIndex, len(eyePrediction)):
            if(eyePrediction[i] < cEyePupilDirectionThreshold):
                eyePrediction[i] = cFalse
            else:
                eyePrediction[i] = cTrue

    return eyePrediction

# check if Face angle fields are above cFaceHasAngle and set it to 1 if above
def correctFacePrediction(facePrediction = []):
    if len(facePrediction):
        for i in range(cFaceAngleStartIndex, cFaceAngleEndIndex):
            if(facePrediction[0][i] < cFaceHasAngle):
                facePrediction[0][i] = cFalse
            else:
                facePrediction[0][i] = cTrue

    return facePrediction

# resize image (img) and normalize it in range (0, 1)
def resizeAndNormalizeImage(img):

    #resize img
    resizedImg = cv2.resize(img, (inputWidth, inputHeight), Image.ANTIALIAS)
    resizedImg = np.asarray(resizedImg)

    #normalize img
    normalizedImg = resizedImg/255

    return normalizedImg

# try opening video source
def captureStart(vsource = 0):

    cap = None

    # try to open video source, if not wait and try again
    while(cap is None or cap.isOpened() == False):
        if(isinstance(vsource, int)):
            cap = cv2.VideoCapture(vsource + cv2.CAP_DSHOW)
            width  = cap.get(cCVwidth)  # float
            height = cap.get(cCVheight) # float
            change_res(cap, cResolutionWidth, cResolutionHeight)
        else:
            cap = cv2.VideoCapture(vsource)

        if(cap is None or cap.isOpened() == False):
            print("Error opening video source")
            cap.release()

        sleep(2)

    return cap

# moving average function
def movingAverage(readings, reading, windowSize):
    readings.append(reading)

    avg = np.mean(readings, axis = 0)

    if(len(readings) == windowSize):
        readings = readings[1:]

    return avg, readings

# attention logic run in another thread
def checkAttention(): 
    global eyesAttentionList
    global faceAttentionList

    # how many frames in cTimeInterval have 'eyeClosed' prediction set to 1
    leftEyeFramesOpen = 0
    rightEyeFramesOpen = 0

    # how many frames in cTimeInterval have Face angle fields prediction set to 1
    faceHasAngle = 0

    # start thread every cTimeInterval seconds
    threading.Timer(cTimeInterval, checkAttention).start()

    # calculate how many frames in cTimeInterval have 'eyeClosed' prediction set to 1
    for i in range(len(eyesAttentionList[cLeftEyeAtt])):
        leftEyeFramesOpen += eyesAttentionList[cLeftEyeAtt][i][cEyeClosed]

    for i in range(len(eyesAttentionList[cRightEyeAtt])):
        rightEyeFramesOpen += eyesAttentionList[cRightEyeAtt][i][cEyeClosed]

    # how many frames in cTimeInterval have Face angle fields prediction set to 1
    for i in range(len(faceAttentionList)):
        for j in range(cFaceAngleStartIndex, cFaceAngleEndIndex):
            faceHasAngle += faceAttentionList[i][0][j]

    # reset state of the eyesAttentionList and faceAttentionList
    eyesAttentionList = [[], []]
    faceAttentionList = []

    # check if attention dropped
    if (leftEyeFramesOpen + rightEyeFramesOpen >= cEyesClosedThreshold or
        faceHasAngle >= cFaceHasAngleThreshold):
        winsound.Beep(cSoundFrequency, cSoundDuration)

# main program loop
def predictFace(vsource = 1):
    global currentFPS
    global eyesAttentionList

    # used for drawing info on frame
    facePredDenorm = []
    faceElementsPredDenorm = []

    # open video source
    cap = captureStart()

    # frame number
    frameId = 0
    
    # video stream window
    cv2.namedWindow(mainWindowName)

    # face and eye windows
    cv2.namedWindow("Left " + eyeWindowName)
    cv2.namedWindow("Right " + eyeWindowName)
    cv2.namedWindow(faceWindowName)

    ########## MOVING AVERAGE ##########
    facePredictionAvg = []
    faceElementsPredAvg = []
    eyesPredictionAvg = []

    faceReadings = []
    faceElementsReadings = []
    leftEyeReadings = []
    rightEyeReadings = []

    # attention logic 
    checkAttention()

    while(cap.isOpened()):
        s_time = time()

        ret, frame = cap.read()
        
        if(ret == True):

            # frame grayscale and prepare for neural network 
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            preparedFrame = resizeAndNormalizeImage(grayFrame)
            
            # predict face
            facePrediction = face_model(preparedFrame[np.newaxis, :, :, np.newaxis], training = False).numpy()
            
            # correct Face angle fields if facePrediction list
            facePrediction = correctFacePrediction(facePrediction)

            # add predictions to attention check list
            faceAttentionList.append(facePrediction)

            # moving average 
            facePredictionAvg, faceReadings = movingAverage(faceReadings, facePrediction, cFaceWindowSize)
            
            # if face is found continue with other predictions
            if(facePredictionAvg[0][cNoFace] < cNoFaceThreshold):
                
                # prepare face for neural network 
                faceImg = cropFace(grayFrame, facePredictionAvg)
                preparedFace = resizeAndNormalizeImage(faceImg)
                
                faceElementsPrediction = face_elements_model(preparedFace[np.newaxis, :, :, np.newaxis], training = False).numpy()
                
                # moving average 
                faceElementsPredAvg, faceElementsReadings = movingAverage(faceElementsReadings, faceElementsPrediction, cFaceElementsWindowSize)

                eyesData = [] 
                lEyePresent = False
                rEyePresent = False
                
                if faceElementsPredAvg[0][cNoLeftEye] < cNoEyeThreshold or faceElementsPredAvg[0][cNoRightEye] < cNoEyeThreshold:
                    
                    leftEyeImg, rightEyeImg = cropEyes(faceImg, faceElementsPredAvg)

                    if faceElementsPredAvg[0][cNoLeftEye] < cNoEyeThreshold and leftEyeImg.shape[0] > 50 and leftEyeImg.shape[1] > 50:
                        # prepare eyes for neural network
                        preparedLeftEye = resizeAndNormalizeImage(leftEyeImg)
                        eyesData.append(preparedLeftEye)
                        lEyePresent = True

                    if faceElementsPredAvg[0][cNoRightEye] < cNoEyeThreshold and rightEyeImg.shape[0] > 50 and rightEyeImg.shape[1] > 50:
                        # prepare eyes for neural network
                        preparedRightEye = resizeAndNormalizeImage(rightEyeImg)
                        eyesData.append(preparedRightEye)
                        rEyePresent = True
                
                # prepare eyes for neural network
                df_im = np.asarray(eyesData)
                df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

                if len(eyesData):
                    eyesPrediction = attention_model(df_im, training = False).numpy()

                eyesPredictionAvg = []
                # check to see if any eye is present and correct noEyes and pupil direction to integer true/false values
                if(lEyePresent and len(eyesPrediction[cEyesDataLeft])):
                    eyesPrediction[cEyesDataLeft] = correctEyesPrediction(eyesPrediction[cEyesDataLeft])
                    # add predictions to attention check list
                    eyesAttentionList[0].append(eyesPrediction[cEyesDataLeft])

                    # moving average 
                    leftEyeAvg, leftEyeReadings = movingAverage(leftEyeReadings, eyesPrediction[cEyesDataLeft], cEyesWindowSize)
                    leftEyeAvg[0] = eyesPrediction[cEyesDataLeft][0]
                    eyesPredictionAvg.append(leftEyeAvg)


                if(rEyePresent and len(eyesPrediction[cEyesDataRight])):
                    eyesPrediction[cEyesDataRight] = correctEyesPrediction(eyesPrediction[cEyesDataRight])
                    # add predictions to attention check list
                    eyesAttentionList[1].append(eyesPrediction[cEyesDataRight])

                    # moving average 
                    rightEyeAvg, rightEyeReadings = movingAverage(rightEyeReadings, eyesPrediction[cEyesDataRight], cEyesWindowSize)
                    rightEyeAvg[0] = eyesPrediction[cEyesDataRight][0]
                    eyesPredictionAvg.append(rightEyeAvg)

                # draw face bounding box and face elements on live stream
                frame, facePredDenorm, faceElementsPredDenorm = drawPredictionOnImage(facePredictionAvg, faceElementsPredAvg, frame, faceImg, eyesPredictionAvg, leftEyeImg, rightEyeImg)

                # draw predictions on face and eyes
                drawEyesOnFace(facePrediction, faceElementsPrediction, faceImg, eyesPrediction)

                # show face
                cv2.imshow(faceWindowName, faceImg)

                # show eyes
                leftEyeImg = np.array(leftEyeImg)
                rightEyeImg = np.array(rightEyeImg)
                if lEyePresent:
                    cv2.imshow("Left " + eyeWindowName, leftEyeImg)
                if rEyePresent:
                    cv2.imshow("Right " + eyeWindowName, rightEyeImg)

            # show main program information
            frame = showInfo(frame, facePrediction[0][0], facePredDenorm, faceElementsPredDenorm)

            # show video stream
            cv2.imshow(mainWindowName, frame)

            frameId += 1

            if(frameId > 60):
                frameId = 0
          
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break
        else:
            break

        e_time = time()
        elapsed = e_time - s_time

        # calculate current frame rate
        currentFPS = int(1 / elapsed)

    cap.release()
    cv2.destroyAllWindows()

# draws eyes predictions on face image
def drawEyesOnFace(facePrediction, faceElementsPrediction, faceImg, eyesPrediction):
    faceElementsPredDenorm = []
    leftEyePredDenorm = []
    rightEyePredDenorm = []

    # denormalize face width 
    faceWDenom = (facePrediction[0][cFaceW] * (minMaxValuesPh01[cMax][cFaceWminMax - 1] - minMaxValuesPh01[cMin][cFaceWminMax - 1]) + minMaxValuesPh01[cMin][cFaceWminMax - 1])

    # copy denormalized face elements to a new array
    faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor = cLabeledFaceHeight / faceImg.shape[0])[0]

    # calculate eye points of interest on faceImg
    topELeftX, topELeftY = eyeCropPoints(faceElementsPredDenorm[cLeftEyeX], faceElementsPredDenorm[cLeftEyeY], faceImg)[0]
    topERightX, topERightY = eyeCropPoints(faceElementsPredDenorm[cRightEyeX], faceElementsPredDenorm[cRightEyeY], faceImg)[0]
  

    # denormalize eyes points of interest
    # faceWDenom * cEyeWidthPerc because eye dimension is 30% of faceWDenom
    if faceElementsPrediction[0][cNoLeftEye] < cNoEyeThreshold:
        leftEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataLeft], faceWDenom * cEyeWidthPerc, 1, 11)
    if faceElementsPrediction[0][cNoRightEye] < cNoEyeThreshold:
        rightEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataRight], faceWDenom * cEyeWidthPerc, 1, 11)

    # calculate eyes points of interest on face image
    for i in range(1, len(leftEyePredDenorm) - 5, 2):
        leftEyePredDenorm[i] += (faceElementsPredDenorm[0] + topELeftX)
        leftEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topELeftY)

    for i in range(1, len(rightEyePredDenorm) - 5, 2):
        rightEyePredDenorm[i] += (faceElementsPredDenorm[0] + topERightX)
        rightEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topERightY)

    color = (0, 0, 0)

    # draw circular points from predicted eyes points of interest on face image
    for i in range(1, len(leftEyePredDenorm) - 4, 2):
        cv2.circle(faceImg, (int(leftEyePredDenorm[i]), int(leftEyePredDenorm[i + 1])), 1, color, 2)

    for i in range(1, len(rightEyePredDenorm) - 4, 2):
        cv2.circle(faceImg, (int(rightEyePredDenorm[i]), int(rightEyePredDenorm[i + 1])), 1, color, 2)

    return faceImg

# shows info on original frame
def showInfo(image, noFacePred, facePredDenorm = [], faceElementsPredDenorm = []):
    faceX, faceY = -1, -1
    leftEyeX, leftEyeY = -1, -1
    rightEyeX, rightEyeY = -1, -1

    if (len(facePredDenorm)):
        faceX, faceY = int(facePredDenorm[0] + 0.5), int(facePredDenorm[1] + 0.5)
    if (len(faceElementsPredDenorm)):
        leftEyeX, leftEyeY = int(faceElementsPredDenorm[2] + 0.5), int(faceElementsPredDenorm[3] + 0.5)
        rightEyeX, rightEyeY = int(faceElementsPredDenorm[4] + 0.5), int(faceElementsPredDenorm[5] + 0.5)

    dateAndTime = "Timestamp: " + "{date:%H:%M:%S %d-%m-%Y}".format(date = datetime.datetime.now())
    faceCoordinates = "Face on: (" + str(faceX) + ", " + str(faceY) + ")"
    leftEyeCoordinates = "Left eye on: (" + str(leftEyeX) + ", " + str(leftEyeY) + ")"
    rightEyeCoordinates = "Right eye on: (" + str(rightEyeX) + ", " + str(rightEyeY) + ")"
    applicationFPS = "FPS: " + str(currentFPS)

    info = dateAndTime + "\n" + faceCoordinates + "\n" + leftEyeCoordinates + "\n" + rightEyeCoordinates + "\n" + applicationFPS

    y0 = 15

    for i, line in enumerate(info.split("\n")):
        y = y0 + i * cInfoDY
        cv2.putText(image, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, infoFontColor, 2)

    if(noFacePred > cNoFaceThreshold):
         cv2.putText(image, "Driver not present", (cDriverInfoX, cDriverInfoY), cv2.FONT_HERSHEY_SIMPLEX, 1.3, driverFontColor, 2)

    return image

# draws all predictions on original image
def drawPredictionOnImage(facePrediction, faceElementsPrediction, image, faceImg, eyesPrediction, leftEyeImg, rightEyeImg):

    faceElementsPredDenorm = []
    leftEyePredDenorm = []
    rightEyePredDenorm = []

    # denormalize face predictions
    [faceXDenom, faceYDenom, faceWDenom] = denormalizeFacePrediction(facePrediction)

    # calculate points for face bounding rectangle to be drawn
    topLeftX = faceXDenom - int((faceWDenom / 2) + 0.5)
    topLeftY = faceYDenom - int(((faceWDenom / 2) * cFaceWidthHeightRatio) + 0.5)

    bottomRightX = faceXDenom + int((faceWDenom / 2) + 0.5)
    bottomRightY = faceYDenom + int(((faceWDenom / 2) * cFaceWidthHeightRatio) + 0.5)

    # denormalize face elements to a new array
    faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor = cLabeledFaceHeight / faceImg.shape[0])[0]
    
    # denormalize eyes points of interest
    # faceWDenom * cEyeWidthPerc because eye dimension is 30% of faceWDenom
    if len(eyesPrediction) and faceElementsPrediction[0][cNoLeftEye] < cNoEyeThreshold:
        leftEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataLeft], faceWDenom * cEyeWidthPerc, 1, 11)
    if len(eyesPrediction) and faceElementsPrediction[0][cNoRightEye] < cNoEyeThreshold:
        rightEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataRight], faceWDenom * cEyeWidthPerc, 1, 11)

    # calculate eye points of interest on faceImg
    topELeftX, topELeftY = eyeCropPoints(faceElementsPredDenorm[cLeftEyeX], faceElementsPredDenorm[cLeftEyeY], faceImg)[0]
    topERightX, topERightY = eyeCropPoints(faceElementsPredDenorm[cRightEyeX], faceElementsPredDenorm[cRightEyeY], faceImg)[0]
  
    # calculate face elements coordinates on face image
    for i in range(0, len(faceElementsPredDenorm), 2):
        faceElementsPredDenorm[i] += topLeftX
        faceElementsPredDenorm[i + 1] += topLeftY

    # calculate eyes points of interest on original frame
    for i in range(1, len(leftEyePredDenorm) - 5, 2):
        leftEyePredDenorm[i] += (faceElementsPredDenorm[0] + topELeftX)
        leftEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topELeftY)

    for i in range(1, len(rightEyePredDenorm) - 5, 2):
        rightEyePredDenorm[i] += (faceElementsPredDenorm[0] + topERightX)
        rightEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topERightY)

    # draw face bounding rectangle on original frame
    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)), (0,255,0), 2)

    color = (0, 255, 0)

    # check to see if eyes are open 
    # set color to red if eyes are closed
    if (len(eyesPrediction)):
        if(eyesPrediction[cEyesDataLeft][cEyeClosed] or eyesPrediction[cEyesDataRight][cEyeClosed]):
            color = (0, 0, 255)

    # draw circular points from predicted eyes points of interest on original image
    for i in range(1, len(leftEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(leftEyePredDenorm[i]), int(leftEyePredDenorm[i + 1])), 1, color, 2)

    for i in range(1, len(rightEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(rightEyePredDenorm[i]), int(rightEyePredDenorm[i + 1])), 1, color, 2)

    return [image, [faceXDenom, faceYDenom], faceElementsPredDenorm]

if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # disable GPU and work with CPU only
    #my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    #tf.config.set_visible_devices([], 'GPU')

    # Load models
    face_model_name = "model_phase01.h5"
    face_elements_model_name = "model_phase02.h5"
    attention_model_name = "model_phase03.h5"

    face_model = tf.keras.models.load_model(face_model_name)
    face_elements_model = tf.keras.models.load_model(face_elements_model_name)
    attention_model = tf.keras.models.load_model(attention_model_name)

    # load minimal and maximal values for denormalization
    minMaxValuesPh01 = readMinMaxFromCSV(minMaxCSVpath)
    minMaxValuesPh02 = readMinMaxFromCSV(minMaxPhase02)
    minMaxValuesPh03 = readMinMaxFromCSV(minMaxPhase03)

    # predict face from live video source
    predictFace(vSource)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

