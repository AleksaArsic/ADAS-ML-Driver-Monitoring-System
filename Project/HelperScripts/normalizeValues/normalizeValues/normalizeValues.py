import cv2
import math
import random
import datetime
import glob, os
import numpy as np 
import pandas as pd 
from time import time
import os.path
from os import path
import shutil

csvPath = "D:\\Diplomski_all\\test_ph03\\expected_ph03.csv"
minMaxCSVpath = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase03_csv\\trainingSet_phase03_normalized_min_max.csv"

# start and end index for normalization
start = 1
end = 11

# minimal and maximal index in minMaxValuesPh0x
cMin = 0
cMax = 1

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

def loadCategories(categories, catPath):

    filenames = []
    lines = readCSV(catPath)
    cnt = 0
    for line in lines:
        #if len(line)>0:

        if cnt < 2:
           cnt = cnt + 1
           continue

        if (len(line)>0):
            p1 = line.find(',')
            fname = line[0:p1]
            p1 = p1+1

            cat=line[p1:]

            cat = cat.rstrip(',\n')
            cat = cat.split(',')

            cnt_cat = 0
            for item in cat:
                cat[cnt_cat] = float(item)
                cnt_cat = cnt_cat + 1
            cat = np.asarray(cat)

            categories.append(cat)

        cnt = cnt + 1
    print ('loading complete!')
    
    return categories

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
			
			cnt_cat = 0
			for item in cat:
				cat[cnt_cat] = float(item)
				cnt_cat = cnt_cat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result

def showStat(predictions, ph):
    cnt = 0
    c1 = 0
    compare = []

    for i in range(len(predictions)):
        c1 = 0
        ss = ''
        sctg = ''
        for item in predictions[cnt]:
            p = item 
            predictions[cnt][c1] = p
            ss = ss+str(p)+','

            c1 = c1 + 1

        s = ','+ss

        compare.append(s)
        cnt = cnt+1

    with open('phase' + str(ph)+'_normalized_'+str(len(predictions))+'.csv', 'w') as f:
        for item in compare:
            f.write("%s\n" % item)



if __name__ == "__main__":
    script_start = datetime.datetime.now()

    # load minimal and maximal values for normalization
    minMaxValues = readMinMaxFromCSV(minMaxCSVpath)

    # load values 
    csvValues = []
    csvValues = loadCategories(csvValues, csvPath)

    # normalize values
    normalizedValues = []

    for line in csvValues:
        for i in range(start, end):
            line[i] = (line[i] - minMaxValues[cMin][i - 1]) / (minMaxValues[cMax][i - 1] - minMaxValues[cMin][i - 1])

        normalizedValues.append(line)

    # write a new csv
    showStat(csvValues, 3)

    script_end = datetime.datetime.now()
    print (script_end-script_start)