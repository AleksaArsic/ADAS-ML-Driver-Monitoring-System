import numpy as np
import cv2
import time
import random
import os
import glob
import math
import PIL as PIL
from PIL import Image, ImageDraw

inputHeight = 100
inputWidth = 100

start = 0
maxVal = 8000
r = 1

timeConsumptionLabels = ['Frame preprocessing', 'Face prediction', 'Face preprocessing', \
                        'Face elements prediction', 'Face elements preprocessing', \
                        'Eyes prediction', 'Visual notification']

SAMPLE_DIFF_THRESHOLD = 0.1

def denormalizePredictions(minMaxValues, predictions):
    
    for i in range(len(predictions)):
        for j in range(len(minMaxValues[0])):
            minVal = minMaxValues[0][j]
            maxVal = minMaxValues[1][j]

            predictions[i][j] = predictions[i][j] * (maxVal - minVal) + minVal
        
    return 0

def compareResults(testLabels, predictions):

    sampleDifferenceAcc = []
    predictionsAcc = [] 

    # transpose arrays for easier math
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    for i in range(len(predictions)):
        # calculate difference accuracy between samples
        maxRefValue = max(testLabels[i])
    
        if maxRefValue == 0:
            maxRefValue += 0.00001

        if(np.any(testLabels[i] == 0)):
            testLabels[i] += 0.00001

        diff = abs(predictions[i] - testLabels[i]) / testLabels[i]
    
        sampleDifferenceAcc = []
        
        for j in range(len(diff)):
            if(diff[j] <= SAMPLE_DIFF_THRESHOLD):
                sampleDifferenceAcc.append(True)
            else:
                sampleDifferenceAcc.append(False)

        validSamples = 0
        invalidSamples = 0

        for j in range(len(sampleDifferenceAcc)):
            if(sampleDifferenceAcc[j] == True):
                validSamples += 1
            else:
                invalidSamples += 1

        predictionsAcc.append(validSamples / len(predictions[i]))

    # transpose to normal
    testLabels = np.transpose(testLabels)
    predictions = np.transpose(predictions)

    return predictionsAcc

def writeTestToCsv(testLabels, predictions, predictionsAcc):
    s = ''
    i = 0 
    for item in testLabels:
        for field in item:
            s += str(field) 
            s += ','

        s += ','

        l = predictions[i]

        for field in l:
            s += str(field)
            s += ','

        s += '\n'
        i += 1

    s += '\n'

    for item in predictionsAcc:
        s += str(item) + ','

    s += '\n'

    with open('test_predictions_results.csv', 'w') as f:
        f.write(s)

def trainTestDatasetSplit(images, labels):
    testImages = []
    testLabels = []

    datasetLength = len(images)

    testLength = int(datasetLength * 0.1)

    # debug
    indexes = []

    for i in range(testLength):
        #random.seed(time.time())
        n = random.randint(0, datasetLength)

        testImages.append(images[n])
        testLabels.append(labels[n])

        images.pop(n)
        labels.pop(n)

        datasetLength -= 1

        indexes.append(n)

    print(indexes)

    return [testImages, testLabels]

def grayConversion(image):
    grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
    gray_img = grayValue.astype(np.uint8)
    return gray_img

def readCSV(filepath):
    result = []
    dat_file = open(filepath,'r')
    lines=dat_file.readlines()
    for line in lines:
        if len(line)>0:
            p1 = line.find(',')
            filename = line[0:p1]
            categ = line[p1+1:]
            s = filename+','+categ
            result.append(s)
    return result

def loadImages(imgsDir, images):
    print ('loading  images...')

    filenames = []

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        img = Image.open(imagePath)
        img = np.asarray(img)

        images.append(img)
      
        fname = os.path.basename(imagePath)
        filenames.append(fname)

    print ('loading complete!')
    
    return [images, filenames]

def loadImagesAndGrayscale(imgsDir, images, inputWidth = 100, inputHeight = 100):
    print ('loading  images...')

    filenames = []

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        img = Image.open(imagePath)

        img = img.resize((inputWidth,inputHeight), Image.ANTIALIAS)
        img = np.asarray(img)
            
        gray = grayConversion(img)

        img1 = gray/255

        images.append(img1)
      
        fname = os.path.basename(imagePath)
        filenames.append(fname)

    print ('loading complete!')
    
    return [images, filenames]

#def loadImagesAndCategories(images, imgsDir, categories, catPath, minMaxValues, phase = 1, inputWidth = 100, inputHeight = 100):
def loadImagesAndCategories(images, imgsDir, categories, catPath, phase = 1, inputWidth = 100, inputHeight = 100):
    print ('loading  images...')

    filenames = []
    lines = readCSV(catPath)
    cnt = 0
    for line in lines:

        faceX = 0
        faceY = 0
        faceW = 0

        if (len(line)>0):
            p1 = line.find(',')
            fname = line[0:p1]
            p1 = p1+1
            image_path = imgsDir + fname + '.jpg'
            filenames.append(fname)

            cat=line[p1:]

            cat = cat.rstrip(',\n')
            cat = cat.split(',')

            if(phase == 2):
                cat.pop(16)

            if(phase == 3):
                cat.pop(11)
                cat.pop(11)
                cat.pop(11)
                cat.pop(11)
                cat.pop(11)

            cnt_cat = 0
            for item in cat:
                cat[cnt_cat] = float(item)
                cnt_cat = cnt_cat + 1
            cat = np.asarray(cat)


            #phase 1 specific
            faceX = cat[1]
            faceY = cat[2]
            faceW = cat[3]

            categories.append(cat)

            img = Image.open(image_path)

            img = img.resize((inputWidth,inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            
            gray = grayConversion(img)

            img1 = gray/255

            images.append(img1)

        cnt = cnt + 1
    print ('loading complete!')
    
    return [images, categories, filenames]

def showStat(filenames, predictions, ph):
    cnt = 0
    ok_cnt = 0
    c1 = 0
    compare = []
    errors = []

    for fnames in filenames:
        f = filenames[cnt]
        c1 = 0
        ss = ''
        sctg = ''
        for item in predictions[cnt]:
            p = item
            predictions[cnt][c1] = p
            ss = ss+str(p)+','
            c1 = c1 + 1

        if ss==sctg:
            ok_cnt = ok_cnt + 1
        else:
            errors.append(f)

        s = f+','+ss

        compare.append(s)
        cnt = cnt+1

    with open('phase' + str(ph)+'_results_'+str(len(filenames))+'.csv', 'w') as f:
        for item in compare:
            f.write("%s\n" % item)

def readMinMaxFromCSV(filepath):
	
	lines = readCSV(filepath)
	cnt = 0
	result = []
	
	for line in lines:
		if(len(line) > 0):
			#p1 = line.find(',')
			#p1 = p1+1
			#cat=line[p1:]
			cat=line[:]

			cat = cat.rstrip(',\n')
			cat = cat.split(',')
			
			cnt_cat = 0
			for item in cat:
				cat[cnt_cat] = float(item)
				cnt_cat = cnt_cat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result

def drawPredictionsToDisk(predictions, filenames, imgsDir, minMaxValues):

    cnt = 0

    for fname in filenames:
        imagePath = imgsDir + fname

        faceX = predictions[cnt][1]
        faceY = predictions[cnt][2]
        faceW = predictions[cnt][7]
        
        faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
        faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
        faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

        img = Image.open(imagePath)

        img = img.resize((inputWidth,inputHeight), Image.ANTIALIAS)
        img = np.asarray(img)
            
        gray = grayConversion(img)

        result = Image.fromarray((gray).astype(np.uint8))

        topLeftX = faceXDenom - math.ceil((faceWDenom / 2))
        topLeftY = faceYDenom - math.ceil(((faceWDenom / 2) * 1.5))

        topLeftX = math.ceil(topLeftX / 6.4)
        topLeftY = math.ceil(topLeftY / 4.8)

        bottomRightX = faceXDenom + math.ceil((faceWDenom / 2))
        bottomRightY = faceYDenom + math.ceil(((faceWDenom / 2) * 1.5))

        bottomRightX = math.ceil(bottomRightX / 6.4)
        bottomRightY = math.ceil(bottomRightY / 4.8)


        cv2.rectangle(gray, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
        cv2.imwrite('D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_grayscale_predictions\\' + fname + '.jpg', gray)

        cnt = cnt + 1


def drawExpected(grayImg, fname, faceX, faceY, faceW, minMaxValues):
    #denormalize

    faceXDenom = (faceX * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceYDenom = (faceY * (minMaxValues[1][2] - minMaxValues[0][2]) + minMaxValues[0][2])
    faceWDenom = (faceW * (minMaxValues[1][7] - minMaxValues[0][7]) + minMaxValues[0][7])

    result = Image.fromarray((grayImg).astype(np.uint8))

    topLeftX = faceXDenom - math.ceil((faceWDenom / 2))
    topLeftY = faceYDenom - math.ceil(((faceWDenom / 2) * 1.5))

    topLeftX = math.ceil(topLeftX / 6.4)
    topLeftY = math.ceil(topLeftY / 4.8)

    bottomRightX = faceXDenom + math.ceil((faceWDenom / 2))
    bottomRightY = faceYDenom + math.ceil(((faceWDenom / 2) * 1.5))

    bottomRightX = math.ceil(bottomRightX / 6.4)
    bottomRightY = math.ceil(bottomRightY / 4.8)

    #draw rectangle on face
    cv2.rectangle(grayImg, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
    cv2.imwrite('phase01_greyscale\\' + fname + '.jpg', grayImg)


def showAverageTimeConsumption(timeConsumptionArr, timestamp):
    avgResult = []

    for l in timeConsumptionArr:
        avgResult.append(np.average(l))

    avgString = ''
    timeStringArr = []

    for avg in avgResult:
        avgString += str(avg) + ','

    timeCons = np.array(timeConsumptionArr).T.tolist()

    for l in timeCons:
        timeString = ''

        for t in l:
            timeString += str(t) + ','

        timeStringArr.append(timeString)

    with open('averageTimeConsumption_' + str(timestamp) + '.csv', 'w') as f:
        for s in timeConsumptionLabels:
            f.write(s + ',')

        f.write('\n')
        f.write(avgString)

    with open('timeConsumption_' + str(timestamp) + '.csv', 'w') as f:
        for s in timeConsumptionLabels:
            f.write(s + ',')
        
        f.write('\n')

        for item in timeStringArr:
            f.write(item + '\n')
