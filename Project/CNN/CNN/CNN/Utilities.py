import numpy as np
import cv2
import os
import glob
import PIL as PIL
from PIL import Image, ImageDraw

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

def loadImagesAndCategories(images, imgsDir, categories, catPath, minMaxValues, inputWidth = 100, inputHeight = 100):
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
            cat.pop(6)
            cat.pop(6)
            cat.pop(6)
            cat.pop(6)

            cnt_cat = 0
            for item in cat:
                cat[cnt_cat] = float(item)
                cnt_cat = cnt_cat + 1
            cat = np.asarray(cat)

            faceX = cat[0]
            faceY = cat[1]
            faceW = cat[6]

            categories.append(cat)

            img = Image.open(image_path)

            img = img.resize((inputWidth,inputHeight), Image.ANTIALIAS)
            img = np.asarray(img)
            
            gray = grayConversion(img)

            # debug
            drawExpected(gray, fname, faceX, faceY, faceW, minMaxValues)
            
            img1 = gray/255

            images.append(img1)

        cnt = cnt + 1
    print ('loading complete!')
    
    return [images, categories, filenames]

def showStat(filenames, predictions):
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
            #if item>0.5:
            #    p=1
            #else:
            #    p=0
            p = item #predictions[cnt]
            predictions[cnt][c1] = p
            ss = ss+str(p)+','
            #c = categories[cnt][c1]
            #sctg = sctg+str(c)+','
            c1 = c1 + 1

        if ss==sctg:
            ok_cnt = ok_cnt + 1
        else:
            errors.append(f)

        s = f+','+ss

        compare.append(s)
        cnt = cnt+1

    with open('img' + str(r)+'_results_'+'_'+str(start)+'_'+str(start+max)+'.csv', 'w') as f:
        for item in compare:
            f.write("%s\n" % item)

    with open('Accuracy_img' + str(r)+'_results_'+'_'+str(start)+'_'+str(start+max)+'.csv', 'w') as f:
        f.write("Accuracy = %s\n" % str(ok_cnt/cnt))

    with open('errors.csv', 'w') as f:
        for item in errors:
            f.write("%s\n" % item)

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
				cat[cnt_cat] = int(item)
				cnt_cat = cnt_cat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result

def drawPredictionsToDisk(predictions, filenames, imgsDir, minMaxValues):

    cnt = 0

    for fname in filenames:
        imagePath = imgsDir + fname

        faceX = predictions[cnt][0]
        faceY = predictions[cnt][1]
        faceW = predictions[cnt][6]
        
        faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
        faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
        faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

        img = Image.open(imagePath)

        img = img.resize((inputWidth,inputHeight), Image.ANTIALIAS)
        img = np.asarray(img)
            
        gray = Utilities.grayConversion(img)

        result = Image.fromarray((gray).astype(np.uint8))

        topLeftX = faceXDenom - (faceWDenom / 2)
        topLeftY = faceYDenom - ((faceWDenom / 2) * 1.5)

        topLeftX /= 6.4
        topLeftY /= 4.8

        bottomRightX = faceXDenom + (faceWDenom / 2)
        bottomRightY = faceYDenom + ((faceWDenom / 2) * 1.5)

        bottomRightX /= 6.4
        bottomRightY /= 4.8


        cv2.rectangle(gray, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
        cv2.imwrite('D:\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\output_2020_04_17_11_39_49_grayscale_predictions\\' + fname + '.jpg', gray)

        cnt = cnt + 1


def drawExpected(grayImg, fname, faceX, faceY, faceW, minMaxValues):
    #denormalize

    faceXDenom = (faceX * (minMaxValues[1][0] - minMaxValues[0][0]) + minMaxValues[0][0])
    faceYDenom = (faceY * (minMaxValues[1][1] - minMaxValues[0][1]) + minMaxValues[0][1])
    faceWDenom = (faceW * (minMaxValues[1][6] - minMaxValues[0][6]) + minMaxValues[0][6])

    result = Image.fromarray((grayImg).astype(np.uint8))

    topLeftX = faceXDenom - (faceWDenom / 2)
    topLeftY = faceYDenom - ((faceWDenom / 2) * 1.5)

    topLeftX /= 6.4
    topLeftY /= 4.8

    bottomRightX = faceXDenom + (faceWDenom / 2)
    bottomRightY = faceYDenom + ((faceWDenom / 2) * 1.5)

    bottomRightX /= 6.4
    bottomRightY /= 4.8

    #draw rectangle on face
    cv2.rectangle(grayImg, (int(topLeftX),int(topLeftY)), (int(bottomRightX),int(bottomRightY)) , (0,255,0), 2)
    cv2.imwrite('output_2020_04_17_11_39_49_grayscale\\' + fname + '.jpg', grayImg)


