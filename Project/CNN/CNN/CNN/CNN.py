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

import keyboard

workingDirPath = os.path.dirname(os.path.realpath(__file__))
outputImageNamebase = "capture_"

windowName = "Video source"

inputHeight = 100
inputWidth = 100
faceOutputNo = 8
faceElementsOutputNo = 12
attentionOutputNo = 15

phase = 1

imgsDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01"
#minMaxCSVpath = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
#minMaxPhase02 = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase02_csv\\trainingSet_phase02_normalized_min_max.csv"
minMaxCSVpath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01_csv\\trainingSet_phase01_normalized_min_max.csv"
minMaxPhase02 = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase02_csv\\trainingSet_phase02_normalized_min_max.csv"
start = 0
max = 8000

images = []
filenames = []
minMaxValues = []
minMaxValuesPh02 = []
predictions = []

# debug
faceLocation = ''
faceLocationNorm = ''

# time consumption break time
breakTime = 0

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

def denormalizeFaceElements(faceElementsPrediction):

    for i in range(2, len(faceElementsPrediction[0])):
        faceElementsPrediction[0][i] = int((faceElementsPrediction[0][i] * (minMaxValuesPh02[1][i - 2] - minMaxValuesPh02[0][i - 2]) + minMaxValuesPh02[0][i - 2]) + 0.5)

    return faceElementsPrediction

def denormalizeFaceElementsPrediction(faceElementsPrediction, elementWidth, start = 0, end = -1):

    if(faceElementsPrediction.ndim > 1):
        predictions = faceElementsPrediction[0].copy()
    else:
        predictions = faceElementsPrediction.copy()

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

    faceCoords = [topLeftX, topLeftY, bottomRightX, bottomRightY]

    clippedValues = np.clip([topLeftX, topLeftY, bottomRightX, bottomRightY], a_min = 0, a_max = None)

    croppedImage = img[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]
    #croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

    # TO - DO : ADD PADDING IF RATIO IS NOT 3:4
    crocroppedImage = addFacePadding(croppedImage, faceCoords)

    #img = drawPredictionOnImage([predictions[cnt]], img)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #croppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

    return croppedImage

def addFacePadding(img, faceCoords = []):
    croppedImage = []
    height = img.shape[0]
    width = img.shape[1]

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

def cropEyes(faceImg, faceElementsPrediction):
    leftEye = []
    rightEye = []

    topLeft = (0, 0)
    topRight = (0, 0)

    print(faceElementsPrediction)

    faceElementsPrediction = denormalizeFaceElements(faceElementsPrediction)

    print(faceElementsPrediction)


    if faceElementsPrediction[0][0] < 0.5:
        tl, br = cropPoints(faceElementsPrediction[0][2], faceElementsPrediction[0][3], faceImg)
        
        tlX, tlY = tl
        brX, brY = br

        clippedValues = np.clip([int(tlX), int(tlY), int(brX), int(brY)], a_min = 0, a_max = None)
        leftEye = faceImg[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]
        topLeft = tl
    if faceElementsPrediction[0][1] < 0.5:
        tl, br = cropPoints(faceElementsPrediction[0][4], faceElementsPrediction[0][5], faceImg)

        tlX, tlY = tl
        brX, brY = br
        
        clippedValues = np.clip([int(tlX), int(tlY), int(brX), int(brY)], a_min = 0, a_max = None)
        rightEye = faceImg[clippedValues[1]:clippedValues[3], clippedValues[0]:clippedValues[2]]
        topRight = tl

    return [leftEye, rightEye, topLeft, topRight]

def cropPoints(x, y, faceImg):
    # calculate coordinates to crop from
    height, width = faceImg.shape
    
    tlEyeX = x - int(0.15 * width)
    tlEyeY = y - int(0.1 * height)
    brEyeX = x + int(0.15 * width)
    brEyeY = y + int(0.1 * height)

    #tlEyeXdenorm = int((tlEyeX * width) + 0.5)
    #tlEyeYdenorm = int((tlEyeY * (width * 1.5)) + 0.5)
    #brEyeXdenorm = int((brEyeX * width) + 0.5)
    #brEyeYdenorm = int((brEyeY * (width * 1.5)) + 0.5)

    return [(tlEyeX, tlEyeY), (brEyeX, brEyeY)]

def correctEyesPrediction(eyePrediction = []):
    # left and right eye open prediction correct
    if len(eyePrediction):
        if(eyePrediction[0] < 0.5):
            eyePrediction[0] = 0
        else:
            eyePrediction[0] = 1

        for i in range(11, len(eyePrediction)):
            if(eyePrediction[i] < 0.5):
                eyePrediction[i] = 0
            else:
                eyePrediction[i] = 1

    return eyePrediction

def determineLookAngleRay(eyePrediction = []):

    x, y = 0, 0

    if len(eyePrediction):
        if(eyePrediction[11] or eyePrediction[12] or eyePrediction[13] or eyePrediction[14]):

            tempL = -1 if eyePrediction[11] else 0
            tempR = 1 if eyePrediction[12] else 0
            tempU = -1 if eyePrediction[13] else 0
            tempD = 1 if eyePrediction[14] else 0

            x = eyePrediction[3] + 50 * tempL + 50 * tempR
            y = eyePrediction[4] + 50 * tempU + 50 * tempD

        else:
            x = eyePrediction[3]
            y = eyePrediction[4]

    return (x, y)

def createNewOutputDir(dateTimeNow):

    outputDirName = "false_" + dateTimeNow
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    return outputDirName

def predictFace(vsource = 1, savePredictions = False):

    # save frames that are not good 
    saving = False

    width = 0
    height = 0

    s_t, e_t = 0, 0

    if(isinstance(vsource, int)):
        cap = cv2.VideoCapture(vsource + cv2.CAP_DSHOW)
        width  = cap.get(3)  # float
        height = cap.get(4) # float
        change_res(cap, 640, 480)
    else:
        cap = cv2.VideoCapture(vsource)

    if(cap.isOpened() == False):
        print("Error opening video source")

    # frame number
    frameId = 0
    
    cv2.namedWindow(windowName)

    #debug
    cv2.namedWindow("le")
    cv2.namedWindow("re")
    cv2.namedWindow("face")

    consumptionTime = [[], [], [], [], [], [], []]
    startTime = time()

    dirCreated = False


    while(cap.isOpened()): # and (time() - startTime < breakTime)):  
        s_time = time()

        ret, frame = cap.read()
        
        if(ret == True):

            #print(frame.shape)

            # save bad frames
            if (saving):
                if not dirCreated:
                    dateTimeNow = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    outputImageName = outputImageNamebase + dateTimeNow
                    outputDirName = createNewOutputDir(dateTimeNow)

                    dirCreated = True

                cv2.imwrite(os.path.join(workingDirPath, outputDirName, outputImageName + "_{0:0=6d}.jpg").format(frameId), frame)

            s_t = time()
            #grayFrame = Utilities.grayConversion(frame)
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #predict face
            img = cv2.resize(grayFrame, (inputWidth, inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            img1 = img/255
            e_t = time()

            # frame preprocessing TIME
            consumptionTime[0].append(e_t - s_t)

            s_t = time()
            facePrediction = face_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()
            e_t = time()

            #leftEyeImg, rightEyeImg = [], [] 

            #check if there is face in frame
            if(facePrediction[0][0] < 0.5):

                # face prediction TIME
                consumptionTime[1].append(e_t - s_t)

                s_t = time()
                faceImg = cropFace(grayFrame, facePrediction)
                cv2.imshow("face", faceImg)

                # predict face elements
                img = cv2.resize(faceImg, (inputWidth, inputHeight), Image.ANTIALIAS)
                img = np.asarray(img)
                img1 = img/255
                e_t = time()

                # face preprocessing TIME
                consumptionTime[2].append(e_t - s_t)

                s_t = time()
                faceElementsPrediction = face_elements_model(img1[np.newaxis, :, :, np.newaxis], training = False).numpy()
                e_t = time()

                # face elements prediction TIME
                consumptionTime[3].append(e_t - s_t)

                s_t = time()

                eyesData = [] 
                lEyePresent = False
                rEyePresent = False
                #leftEyeImg, rightEyeImg = [], []
                #topELeft, topERight = 0, 0
                
                if faceElementsPrediction[0][0] < 0.4 or faceElementsPrediction[0][1] < 0.4:
                    leftEyeImg, rightEyeImg, topELeft, topERight = cropEyes(faceImg, faceElementsPrediction)

                    
                    #eyesData = []

                    if faceElementsPrediction[0][0] < 0.4 and leftEyeImg.shape[0] > 20 and leftEyeImg.shape[1] > 20:
                        img = cv2.resize(leftEyeImg, (inputWidth, inputHeight), Image.ANTIALIAS)
                        img = np.asarray(img)
                        img1 = img/255

                        eyesData.append(img1)
                        lEyePresent = True

                    if faceElementsPrediction[0][1] < 0.4 and rightEyeImg.shape[0] > 20 and rightEyeImg.shape[1] > 20:
                        img = cv2.resize(rightEyeImg, (inputWidth, inputHeight), Image.ANTIALIAS)
                        img = np.asarray(img)
                        img1 = img/255
                                
                        eyesData.append(img1)
                        rEyePresent = True
                #leftEyePrediction = []
                #rightEyePrediction = []


                #if len(leftEyeImg):
                    
                #if len(rightEyeImg):

                df_im = np.asarray(eyesData)
                df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)
                e_t = time()

                # face elements preprocessing TIME
                consumptionTime[4].append(e_t - s_t)

                s_t = time()
                if len(eyesData):
                    eyesPrediction = attention_model(df_im, training = False).numpy()
                e_t = time()

                # eyes prediction TIME
                consumptionTime[5].append(e_t - s_t)

                s_t = time()
                if(lEyePresent and len(eyesPrediction[0])):
                    eyesPrediction[0] = correctEyesPrediction(eyesPrediction[0])
                if(rEyePresent and len(eyesPrediction[-1])):
                    eyesPrediction[-1] = correctEyesPrediction(eyesPrediction[-1])

                # draw face bounding box and face elements on live stream
                drawPredictionOnImage(facePrediction, faceElementsPrediction, frame, eyesPrediction, topELeft, topERight) #, [lEyePresent, rEyePresent])


                leftEyeImg = np.array(leftEyeImg)
                rightEyeImg = np.array(rightEyeImg)
                if lEyePresent:
                    cv2.imshow("le", leftEyeImg)
                if rEyePresent:
                    cv2.imshow("re", rightEyeImg)

            cv2.imshow(windowName, frame)
            frameId += 1
            e_t = time()
          
            # visual notification TIME
            consumptionTime[6].append(e_t - s_t)

            if(savePredictions):
                predictions.append(facePrediction)

            if(keyboard.is_pressed('s')):
                saving = not saving
                while keyboard.is_pressed("s"):
                    pass

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

    Utilities.showAverageTimeConsumption(consumptionTime, breakTime)
    cap.release()
    cv2.destroyAllWindows()

def drawPredictionOnImage(facePrediction, faceElementsPrediction, image, eyesPrediction, topELeft, topERight):
    #debug
    global faceLocation
    global faceLocationNorm

    faceElementsPredDenorm = []
    leftEyePredDenorm = []
    rightEyePredDenorm = []

    faceXDenom = (facePrediction[0][1] * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
    faceYDenom = (facePrediction[0][2] * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceWDenom = (facePrediction[0][7] * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    topLeftX = faceXDenom - int((faceWDenom / 2) + 0.5)
    topLeftY = faceYDenom - int(((faceWDenom / 2) * 1.5) + 0.5)

    bottomRightX = faceXDenom + int((faceWDenom / 2) + 0.5)
    bottomRightY = faceYDenom + int(((faceWDenom / 2) * 1.5) + 0.5)

    #faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, faceWDenom, start = 2)
    faceElementsPredDenorm = faceElementsPrediction[0]

    # faceWDenom * 0.3 because eye dimension is 30% of faceWDenom
    if faceElementsPrediction[0][0] < 0.5:
        leftEyePredDenorm = denormalizeFaceElementsPrediction(eyesPrediction[0], faceWDenom * 0.3, 1, 11)
    if faceElementsPrediction[0][1] < 0.5:
        rightEyePredDenorm = denormalizeFaceElementsPrediction(eyesPrediction[-1], faceWDenom * 0.3, 1, 11)

    for i in range(0, len(faceElementsPredDenorm), 2):
        faceElementsPredDenorm[i] += topLeftX
        faceElementsPredDenorm[i + 1] += topLeftY

    for i in range(1, len(leftEyePredDenorm) - 5, 2):
        leftEyePredDenorm[i] += (faceElementsPredDenorm[0] + topELeft[0])
        leftEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topELeft[1])

    for i in range(1, len(rightEyePredDenorm) - 5, 2):
        rightEyePredDenorm[i] += (faceElementsPredDenorm[0] + topERight[0])
        rightEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topERight[1])

    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)), (0,255,0), 2)

    color = (0, 255, 0)

    # check to se if eyes are open 
    # needs work
    if(eyesPrediction[0][0] or eyesPrediction[0][0]):
        color = (0, 0, 255)

    for i in range(1, len(leftEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(leftEyePredDenorm[i]), int(leftEyePredDenorm[i + 1])), 1, color, 2)

    for i in range(1, len(rightEyePredDenorm) - 4, 2):
        cv2.circle(image, (int(rightEyePredDenorm[i]), int(rightEyePredDenorm[i + 1])), 1, color, 2)

    leftRayX, leftRayY = determineLookAngleRay(leftEyePredDenorm)
    rightRayX, rightRayY = determineLookAngleRay(rightEyePredDenorm)

    #cv2.line(image, (int(leftEyePredDenorm[3]), int(leftEyePredDenorm[4])), (int(leftRayX), int(leftRayY)), (0, 255, 0), thickness=2)
    #cv2.line(image, (int(rightEyePredDenorm[3]), int(rightEyePredDenorm[4])), (int(rightRayX), int(rightRayY)), (0, 255, 0), thickness=2)

    return image

def predictFromImages():

    global images
    global filenames
    global predictions

    [images, filenames] = Utilities.loadImagesAndGrayscale(imgsDir, images, inputWidth, inputHeight)

    df_im = np.asarray(images)
    df_im = df_im.reshape(df_im.shape[0], inputWidth, inputHeight, 1)

    predictions = face_model.predict(df_im, verbose = 1)

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
    minMaxValuesPh02 = Utilities.readMinMaxFromCSV(minMaxPhase02)

    # predict face from live video source
    predictFace(1)

    # predict face from image source
    #predictFromImages()

    #Utilities.showStat(filenames, predictions, 0)
    #Utilities.drawPredictionsToDisk(predictions, filenames, imgsDir, minMaxValues)

    script_end = datetime.datetime.now()
    print (script_end-script_start)

