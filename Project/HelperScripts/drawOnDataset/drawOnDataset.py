import os 
import sys 
import glob
import cv2
import numpy as np

# dataset .csv path
datasetCSVPath = r'C:\Users\arsic\Desktop\master\Rad\output.csv'
# dataset image path
datasetImagePath = r'C:\Users\arsic\Desktop\master\Rad\output'

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

def parseCSV(filepath):
    lines = readCSV(filepath)
    cnt = 0
    result = []

    for line in lines:
        if len(lines) > 0:
            p1 = line.find(',')
            p1 = p1 + 1
            cat = line[p1:]

            cat = cat.rstrip(',\n')
            cat = cat.split(',')

            cntCat = 0

            for item in cat:
                    cat[cntCat] = float(item)
                    cntCat = cntCat + 1

            cat = np.asarray(cat)

            result.append(cat)

    return result

def loadImages(imgsDir, images):

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        img = cv2.imread(imagePath)
        img = np.asarray(img)

        images.append(img)
    
    return images

def drawOnImage(image, predictions):
    # draw face bounding rectangle on original frame
    # calculate points for face bounding rectangle to be drawn
    topLeftX = int(predictions[0]) - int((predictions[2] / 2) + 0.5)
    topLeftY = int(predictions[1]) - int(((predictions[2] / 2) * 1.5) + 0.5)

    bottomRightX = int(predictions[0]) + int((predictions[2] / 2) + 0.5)
    bottomRightY = int(predictions[1]) + int(((predictions[2] / 2) * 1.5) + 0.5)

    color = (0, 255, 0)
    cv2.rectangle(image, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)), color, 2)

    # draw circular points from predicted eyes points of interest on original image
    for i in range(4, 15, 2):
        cv2.circle(image, (int(predictions[i]), int(predictions[i + 1])), 1, color, 2)

    for i in range(15, len(predictions), 2):
        cv2.circle(image, (int(predictions[i]), int(predictions[i + 1])), 1, color, 2)

if __name__ == "__main__":

    images = []
    datasetCSV = []

    datasetCSV = parseCSV(datasetCSVPath)

    images = loadImages(datasetImagePath, images)

    for i in range(len(images)):
        drawOnImage(images[i], datasetCSV[i])

        cv2.imshow('dataset', images[i])

        #if(cv2.waitKey(42) & 0xFF == ord('q')):
        if(cv2.waitKey(80) & 0xFF == ord('q')):
            break