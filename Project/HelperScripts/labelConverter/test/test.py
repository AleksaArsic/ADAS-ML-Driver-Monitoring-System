import os
import sys
import cv2
import glob
import PIL
import numpy as np

# path to images
imagesPath = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase01'

# path to .csv files with minimal and maximal values used for denormalization
minMaxCSVpath = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase01_csv\trainingSet_phase01_normalized_min_max.csv'
minMaxPhase02 = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase02_csv\trainingSet_phase02_normalized_min_max.csv'
minMaxPhase03 = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase03_csv\trainingSet_phase03_normalized_min_max.csv'

# path to normalized .csv labels
normalizedPh01Path = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase01_csv\trainingSet_phase01_normalized.csv'
normalizedPh02Path = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase02_csv\trainingSet_phase02_normalized.csv'
normalizedPh03Path = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase03_csv\trainingSet_phase03_normalized.csv'

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

# neural network input specifics
inputHeight = 100
inputWidth = 100
faceOutputNo = 8
faceElementsOutputNo = 16
attentionOutputNo = 15

# find common labels among two labeled datasets
# find based on common image name
def findCommonLabels(labels1, labels2, labels3):

    print("[*] Finding common label names ...")

    result = []

    for i in range(0, len(labels1)):
        l = []
        l.append(labels1[i])
        for j in range(0, len(labels2)):
            if (labels1[i][0] in labels2[j][0]):
                l.append(labels2[j])
                for k in range(0, len(labels3)):
                    if(labels2[j][0] in labels3[k][0]):
                        l.append(labels3[k])
                        
        #if only one eye found append second one as ones
        if(len(l) == 3):
            temp = [1] * len(l[2])
            l.append(temp)
        if (len(l) > 2):
            result.append(l)

    return result

def loadImages(imgsDir, images):
    filenames = []

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        #img = Image.open(imagePath)
        img = cv2.imread(imagePath)
        img = np.asarray(img)

        images.append(img)
      
        fname = os.path.basename(imagePath)
        filenames.append(fname)
    
    return [images, filenames]

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

def readNormalizedLabels(filepath, phase = 1):
    #normalizedLabels = readCSV(filepath)

    result = parseCSV(filepath, phase)

    if phase == 1:
        a = len(result[0])
    elif phase == 2:
        a = 3
        for i in range(len(result)):
            result[i] = result[i][:-1]
    else:
        a = len(result[0])

    return result

# used for parsing .csv files with minimal and maximal values
# used for normalization and denormalization
def parseCSV(filepath, mode = 0):
	
    lines = readCSV(filepath)
    cnt = 0
    result = []

    for line in lines:
        if(cnt < 2):
            cnt = cnt + 1
            continue

        if len(lines) > 0:
            if mode == 0:
                p1 = line.find(',')
                p1 = p1 + 1
                cat = line[p1:]
            else:
                cat = line[:]

            cat = cat.rstrip(',\n')
            cat = cat.split(',')

            cntCat = 0

            for item in cat:
                if(mode == 0):
                    cat[cntCat] = float(item)
                    cntCat = cntCat + 1

            cat = np.asarray(cat)

            result.append(cat)

    return result

# denormalize eyes prediction
# does not change original prediction array
def denormalizeEyesPrediction(faceElementsPrediction, elementWidth, start = 0, end = -1):

    predictions = faceElementsPrediction.copy()
    predictions = np.array(predictions)

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

# denormalize face elements predictions from normalized range (0, 1) to pixel values of the face image
# changes are made directly to original prediction array
def denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor):

    faceElementsPredDenorm = []

    faceElementsPredDenorm.append(faceElementsPrediction[0][0])
    faceElementsPredDenorm.append(faceElementsPrediction[0][1])

    for i in range(2, len(faceElementsPrediction[0]) - 4):
        faceElementsPredDenorm.append(int(((faceElementsPrediction[0][i] * (minMaxValuesPh02[1][i - 2] - minMaxValuesPh02[0][i - 2]) + minMaxValuesPh02[0][i - 2]) / resizeFactor) + 0.5))

    return [faceElementsPredDenorm]

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

# x - coordinate of eye centre
# y - coordinate of eye centre
def eyeCropPoints(x, y, faceW):
    # calculate coordinates to crop from
    height, width = int(faceW * cFaceWidthHeightRatio), int(faceW)
    
    tlEyeX = x - int(cEyeWidthPerc / 2 * width)
    tlEyeY = y - int(cEyeHeightPerc / 2 * height)
    brEyeX = x + int(cEyeWidthPerc / 2 * width)
    brEyeY = y + int(cEyeHeightPerc / 2 * height)

    return [(tlEyeX, tlEyeY), (brEyeX, brEyeY)]

# draws all predictions on original image
def translateLabels(facePrediction, faceElementsPrediction, eyesPrediction):

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
    faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor = cLabeledFaceHeight / int(faceWDenom * cFaceWidthHeightRatio))[0]
    
    # denormalize eyes points of interest
    # faceWDenom * cEyeWidthPerc because eye dimension is 30% of faceWDenom
    if len(eyesPrediction) and faceElementsPrediction[0][cNoLeftEye] < cNoEyeThreshold:
        leftEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataLeft], faceWDenom * cEyeWidthPerc, 1, 11)
    if len(eyesPrediction) and faceElementsPrediction[0][cNoRightEye] < cNoEyeThreshold:
        rightEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataRight], faceWDenom * cEyeWidthPerc, 1, 11)

    # calculate eye points of interest on faceImg
    topELeftX, topELeftY = eyeCropPoints(faceElementsPredDenorm[cLeftEyeX], faceElementsPredDenorm[cLeftEyeY], faceWDenom)[0]
    topERightX, topERightY = eyeCropPoints(faceElementsPredDenorm[cRightEyeX], faceElementsPredDenorm[cRightEyeY], faceWDenom)[0]
  
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

    return [faceXDenom, faceYDenom, faceWDenom, faceElementsPredDenorm, leftEyePredDenorm, rightEyePredDenorm]

def stripImageNames(commonLabels = []):
    if not len(commonLabels):
        print("[*] commonLabels empty!")
        return -1
    else:
        
        for i in range(len(commonLabels)):
            facePrediction = commonLabels[i][0]
            faceElementsPrediction = commonLabels[i][1]
            eyesPrediction = [commonLabels[i][2][0], commonLabels[i][2][-1]]

            facePrediction = facePrediction[1:]
            faceElementsPrediction = faceElementsPrediction[1:]
            eyesPrediction[i][2][0] = eyesPrediction[i][2][0][1:]
            eyesPrediction[i][2][1] = eyesPrediction[i][2][1][1:]

            commonLabels[i][0] = facePrediction
            commonLabels[i][1] = faceElementsPrediction
            


if __name__ == "__main__":

    # load minimal and maximal values for denormalization
    minMaxValuesPh01 = parseCSV(minMaxCSVpath)
    minMaxValuesPh02 = parseCSV(minMaxPhase02)
    minMaxValuesPh03 = parseCSV(minMaxPhase03)

    # load normalized .csv
    normalizedPh01 = readNormalizedLabels(normalizedPh01Path, 1)
    normalizedPh02 = readNormalizedLabels(normalizedPh02Path, 2)
    normalizedPh03 = readNormalizedLabels(normalizedPh03Path, 3)

    # find common labels
    commonLabels = findCommonLabels(normalizedPh01, normalizedPh02, normalizedPh03)

    # strip image names from commonLabels

    for i in range(len(commonLabels)):

        facePrediction = [commonLabels[i][0]]
        faceElementsPrediction = [commonLabels[i][1]]
        eyesPrediction = [commonLabels[i][2][0], commonLabels[i][2][-1]]

        # translate labels
        result = translateLabels(facePrediction, faceElementsPrediction, eyesPrediction)

        print(result)