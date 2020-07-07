import os
import sys
import cv2
import PIL
from PIL import Image
import numpy as np

if __name__ == "__main__":
	img = Image.open("D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\trainingSet_phase01\\capture_2020_04_17_11_39_49_7263.jpg")
	img = np.array(img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	cv2.imshow('original', img)
	cv2.waitKey(0)