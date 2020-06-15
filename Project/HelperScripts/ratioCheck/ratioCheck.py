import numpy as np
import os 
import cv2
import glob 
import PIL
from PIL import Image 

imgsDir = "C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\phase01_faces_02\\"
images = []

def loadImages(imgsDir, images):
    print ('loading  images...')

    filenames = []

    os.chdir(imgsDir)
    for imagePath in glob.glob("*.jpg"):
        img = Image.open(imagePath)
        img = np.asarray(img)

        images.append(img)
      
        fname = os.path.basename(imagePath)
        #fname = os.path.splitext(fname)[0]
        filenames.append(fname)

    print ('loading complete!')
    
    return [images, filenames]

if __name__ == "__main__":
    
    [images, filenames] = loadImages(imgsDir, images)
    
    ratios = []
    
    for img in images:
        width = img.shape[1]
        height = img.shape[0]
        
        ratios.append(height / width)
        
        
    with open('ratioCheck.csv', 'w') as f:
        for item in ratios:
            f.write("%s\n" % ratios)