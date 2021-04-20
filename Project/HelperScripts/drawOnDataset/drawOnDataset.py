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

def loadImages(imgsDir, images):

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        img = cv2.imread(imagePath)
        img = np.asarray(img)

        images.append(img)
    
    return images

def drawOnImage(image):
    pass

if __name__ == "__main__":

    images = []
    datasetCSV = []

    datasetCSV = readCSV(datasetCSVPath)

    images = loadImages(datasetImagePath, images)

    for image in images:
        cv2.imshow('dataset', image)

        if(cv2.waitKey(42) & 0xFF == ord('q')):
            break