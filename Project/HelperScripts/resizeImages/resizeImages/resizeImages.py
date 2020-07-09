import sys 
import cv2
import glob
import PIL as PIL
from PIL import Image, ImageDraw
import os
from os import path
import shutil
import numpy as np

imgsDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase03\\"
#imgsDir = "C:\\Users\\Cisra\\Desktop\\Diplomski_all\\phase02_test\\"
outputDir = "D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\newPhase03\\"
#outputDir = "C:\\Users\\Cisra\\Desktop\\Diplomski_all\\test_ph02\\"
width = 100
height = 100

def loadAndResize(imgsDir, images):
	print ('loading  images...')

	filenames = []

	os.chdir(imgsDir)
	for imagePath in glob.glob("*.jpg"):
		img = Image.open(imagePath)

		img = img.resize((width,height), Image.ANTIALIAS)
		img = np.asarray(img)

		images.append(img)

		fname = os.path.basename(imagePath)
		filenames.append(fname)

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		cv2.imwrite(outputDir + fname, img)


	print ('loading complete!')

	return [images, filenames]

if __name__ == "__main__":

	if path.exists(outputDir):
		shutil.rmtree(outputDir)

	os.mkdir(outputDir)

	images = []
	[images, filenames] = loadAndResize(imgsDir, images)
