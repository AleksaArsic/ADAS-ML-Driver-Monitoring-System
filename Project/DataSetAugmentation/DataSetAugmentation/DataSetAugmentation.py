import os 
import sys
import cv2
import numpy as np
from PIL import Image
import argparse
from shutil import copyfile
import datetime
from time import time

inputFolder = ""
outputFolder = ""
inputCSV = ""
outputImageNamebase = "capture_"

noOfImages = 0

lr = 0
ud = 0

def shiftImage(image, lr, ud):
    a = 1
    b = 0
    c = lr #left/right (i.e. 5/-5)
    d = 0
    e = 1
    f = ud #up/down (i.e. 5/-5)
    img = image.transform(image.size, Image.AFFINE, (a, b, c, d, e, f))

    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img

def gaussianNoise(img):

    gauss = np.random.normal(0, 0.3, img.size)
    gauss = gauss.reshape(img.shape[0], img.shape[1], img.shape[2]).astype("uint8")

    img_gauss = cv2.add(img, gauss)
    img_gauss = cv2.cvtColor(img_gauss, cv2.COLOR_RGB2BGR)

    return img_gauss

def horizontalFlip(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    h_flipped = cv2.flip(img, 1)

    return h_flipped



def argParser():

    global inputFolder
    global outputFolder
    global inputCSV
    global noOfImages
    global lr
    global ud

    retVal = ""

    argsOK = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "Input folder", required = True)
    parser.add_argument("-o", "--output", help = "Output folder", required = True)
    parser.add_argument("-icsv","--input_csv", help = "Input csv", required = True)
    parser.add_argument("-m", "--mode", help = "Mode: shift", required = True)
    parser.add_argument("-n", "--no_of_imgs", help = "Number of input images", required = False)
    parser.add_argument("-lr", "--left_right", help = "left/right (5/-5)", required = False)
    parser.add_argument("-ud", "--up_down", help = "up/down (5/-5)", required = False)

    args = vars(parser.parse_args())

    try:

        if(len(args["input"]) and len(args["output"]) and len(args["input_csv"])):
            inputFolder = args["input"]
            outputFolder = args["output"]
            inputCSV = args["input_csv"]
        else:
            argsOK = False

        if (args["mode"] == 'shift' and argsOK):
            #shift 
            retVal = "shift"

            if(len(args["left_right"]) or len(args["up_down"])):
                if(len(args["left_right"])):
                    lr = int(args["left_right"])
                if(len(args["up_down"])):
                    ud = int(args["up_down"])
            else:
                argsOK = False
        elif(args["mode"] == "gaussian_noise"):
            retVal = "gaussian_noise"
        elif(args["mode"] == "horizontal_flip"):
            retVal = "h_flip"
        else:
            argsOK = False;

        count = len(args["no_of_imgs"]) if args["no_of_imgs"] else 0

        if(count):
            noOfImages = int(args["no_of_imgs"])
        if not argsOK:
            print("Usage: DataSetAugmentation.py -i <input_folder> -o <output_folder> -icsv <input_csv> -m <mode> [-lr <left_right>, -ud <up_down>]")
            sys.exit(ARG_ERR)

    except SystemExit as e:
        if e.code != ARG_ERR:
            raise
        else:
            os._exit(ARG_ERR)

    return retVal

def loadImages(inputFolder):
    images=os.listdir(inputFolder)
    for fichier in images[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".jpg")):
            images.remove(fichier)

    imagePath = []

    for i in range(len(images)):
        imagePath.append(os.path.join(inputFolder, images[i]))

    return images, imagePath



if __name__ == "__main__":

    #load image
    #img = cv2.imread('capture_2020_06_04_11_10_49_2109.jpg')
    #img = np.array(img)

    #noise = noisy("gauss", img)


    #noisy_sigma = 100
    #noisy_image = add_gaussian_noise(img, noisy_sigma)

    #shiftRight(img)


    #m = (25,25,25) 
    #s = (25,25,25)
    #cv2.randn(img,m,s);


    # parse arguments
    mode = argParser()

    print("Processing images...")

    s_t = datetime.datetime.now()

    #load images
    images, imagePath = loadImages(inputFolder)
    #print(images)

    #create output folder if there is none
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    else:
        os._exit(1)
    #copy old images
    for i in range(len(imagePath)):
        copyfile(imagePath[i], os.path.join(outputFolder, images[i]))

    #augment images
    dateTimeNow = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    outputImageName = outputImageNamebase + dateTimeNow
    newImageNames = []

    #parse input .csv file
    csvFile = open(inputCSV, "r")

    parsed = []
    parsed_old = []

    for line in csvFile:
        parsed_old.append(line)
        separated = line.split(",")
        parsed.append(separated)

    csvFile.close()

    end = len(images)
    if noOfImages != 0:
        end = noOfImages

    parsed = parsed[:end + 2]

    if mode == "shift":
        print("Shifting images.")
        for i in range(end):
            img = Image.open(imagePath[i])
            img = shiftImage(img, lr, ud)
            outputName = os.path.join("", outputImageName + "_{0:0=6d}.jpg").format(i)
            cv2.imwrite(os.path.join(outputFolder, outputName), img) 
            newImageNames.append(outputName)


        for i in range(2, len(newImageNames) + 2):
            parsed[i][0] = newImageNames[i - 2]

        #augment coordinates
        cnt = 0
        for line in parsed:
            if cnt < 2:
                cnt += 1
                continue

            for i in range(2, 8):
                if(i % 2 == 0):
                    line[i] = str(int(line[i]) - lr)
                else:
                    line[i] = str(int(line[i]) - ud)

    elif mode == "gaussian_noise":
        print("Adding Gaussian noise to images.")

        for i in range(end):
            img = Image.open(imagePath[i])
            img = np.asarray(img)
            img = gaussianNoise(img)
            outputName = os.path.join("", outputImageName + "_{0:0=6d}.jpg").format(i)
            cv2.imwrite(os.path.join(outputFolder, outputName), img) 
            newImageNames.append(outputName)

        for i in range(2, len(newImageNames) + 2):
            parsed[i][0] = newImageNames[i - 2]

    elif mode == "h_flip":
        print("Horizontal flipping images.")

        for i in range(end):
            img = Image.open(imagePath[i])
            img = np.asarray(img)
            img = horizontalFlip(img)
            outputName = os.path.join("", outputImageName + "_{0:0=6d}.jpg").format(i)
            cv2.imwrite(os.path.join(outputFolder, outputName), img) 
            newImageNames.append(outputName)

        #augment coordinates
        cnt = 0
        for line in parsed:
            if cnt < 2:
                cnt += 1
                continue

            for i in range(2, 8):
                #cast to string at end
                if(i % 2 == 0):
                    line[i] = str(int(((1 - (int(line[i]) / img.shape[1])) * img.shape[1]) + 0.5))

        #img = Image.open("C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Project\\DataSetAugmentation\\DataSetAugmentation\\capture_2020_04_17_11_39_49_7213.jpg")
        #img = np.array(img)
        
        #h_flip_img = horizontalFlip(img)

        #cv2.imwrite(os.path.join("", "h_flipped.jpg"), h_flip_img) 

        #cv2.imshow('Flipped horizontal image', h_flip_img)

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


    #construct and save new .csv file
    newCsv = []
    for line in parsed:
        l = ','.join(line)
        newCsv.append(l)

    newCSVfile = open(outputFolder + ".csv", "w+")

    for line in parsed_old:
        newCSVfile.write("%s" % line)

    newCsv.pop(0)
    newCsv.pop(0)
    for line in newCsv:
        newCSVfile.write("%s" % line)


    e_t = datetime.datetime.now()

    print("Done.")
    print("Time used: " + str(e_t - s_t))
    print("Images processed: " + str(len(images)))