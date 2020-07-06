import sys 
import cv2
import glob
import PIL as PIL
from PIL import Image, ImageDraw
import os
from os import path
import shutil
import numpy as np

oldCSVPath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase02_csv\\trainingSet_phase02.csv"
newCSVPath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\new_trainingSet_phase02"

oldImgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase02\\"
newImgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\newPhase02\\"

start = 2
end = 11

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

def loadImagesAndCategories(images, imgsDir, categories, catPath):
    print ('loading  images...')

    filenames = []
    lines = readCSV(catPath)
    cnt = 0
    for line in lines:
        #if len(line)>0:

        if cnt < 2:
           cnt = cnt + 1
           continue

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

            cnt_cat = 0
            for item in cat:
                cat[cnt_cat] = float(item)
                cnt_cat = cnt_cat + 1
            cat = np.asarray(cat)

            categories.append(cat)

            img = Image.open(image_path)
            img = np.asarray(img)

            images.append(img)

        cnt = cnt + 1
    print ('loading complete!')
    
    return [images, categories, filenames]

if __name__ == "__main__":
	
    oldImages=[]
    oldCategories = []
    [oldImages, oldCategories, filenames] = loadImagesAndCategories(oldImages, oldImgsDir, oldCategories, oldCSVPath)

    newImages=[]
    newCategories = []
    [newImages, newCategories, filenames] = loadImagesAndCategories(newImages, newImgsDir, newCategories, oldCSVPath)

    cnt = 0
    for i in range(len(oldImages)):
        heightOld = oldImages[i].shape[0]
        widthOld = oldImages[i].shape[1]

        heightNew = newImages[i].shape[0]
        widthNew = newImages[i].shape[1]

        heightFactor = heightNew / heightOld
        widthFactor = widthNew / widthOld

        padY = (heightNew - (heightFactor * heightOld)) / 2;
        padX = (widthNew - (widthFactor * widthOld)) / 2;

        for j in range(start, end, 2):
            newCategories[cnt][j] = int(((newCategories[cnt][j] * widthFactor) + padX) + 0.5)
            newCategories[cnt][j + 1] = int(((newCategories[cnt][j + 1] * heightFactor) + padY) + 0.5)

        cnt += 1


    newCsv = []
    cnt = 0
    for line in newCategories:
        line = np.char.mod('%d', line)
        line = np.concatenate([[filenames[cnt]], line])
        l = ','.join(line)
        newCsv.append(l)
        cnt += 1

    newCSVfile = open(newCSVPath + ".csv", "w+")

    for line in newCsv:
        newCSVfile.write("%s\n" % line)

    newCSVfile.close()
