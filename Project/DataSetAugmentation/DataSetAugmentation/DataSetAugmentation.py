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

lr = 0
ud = 0

def randomNoise(image):
    row, col, ch = image.shape

    noise = np.random.randint(5, size = (row, col, ch), dtype = 'uint32')
    noise = noise.reshape(row, col, ch)

    noisy = image + noise
    noisy_img_clipped = np.clip(noisy, 0, 255)

    return noisy_img_clipped

def noisy(noise_typ,image):
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
    return noisy

def add_gaussian_noise(image_in, noise_sigma):
    temp_image = np.float64(np.copy(image_in))

    h = temp_image.shape[0]
    w = temp_image.shape[1]
    noise = np.random.randn(h, w) * noise_sigma

    noisy_image = np.zeros(temp_image.shape, np.float64)
    if len(temp_image.shape) == 2:
        noisy_image = temp_image + noise
    else:
        noisy_image[:,:,0] = temp_image[:,:,0] + noise
        noisy_image[:,:,1] = temp_image[:,:,1] + noise
        noisy_image[:,:,2] = temp_image[:,:,2] + noise

    """
    print('min,max = ', np.min(noisy_image), np.max(noisy_image))
    print('type = ', type(noisy_image[0][0][0]))
    """

    return noisy_image

def convert_to_uint8(image_in):
    temp_image = np.float64(np.copy(image_in))
    cv2.normalize(temp_image, temp_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)

    return temp_image.astype(np.uint8)

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


def argParser():

    global inputFolder
    global outputFolder
    global inputCSV
    global lr
    global ud

    retVal = ""

    argsOK = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "Input folder", required = True)
    parser.add_argument("-o", "--output", help = "Output folder", required = True)
    parser.add_argument("-icsv","--input_csv", help = "Input csv", required = True)
    parser.add_argument("-m", "--mode", help = "Mode: shift", required = True)
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
        else:
            argsOK = False;

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

    s_t = time()

    #load images
    images, imagePath = loadImages(inputFolder)
    #print(images)

    #create output folder if there is none
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    else:
        sys.exit()
    #copy old images
    for i in range(len(imagePath)):
        copyfile(imagePath[i], os.path.join(outputFolder, images[i]))


    #augment images
    dateTimeNow = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    outputImageName = outputImageNamebase + dateTimeNow
    newImageNames = []

    if mode == "shift":
        for i in range(len(imagePath)):
            img = Image.open(imagePath[i])
            img = shiftImage(img, lr, ud)
            outputName = os.path.join("", outputImageName + "_{:d}.jpg").format(i)
            cv2.imwrite(os.path.join(outputFolder, outputName), img) 
            newImageNames.append(outputName)

        #copy content of old csv file to new one 
        csvFile = open(inputCSV, "r")

        parsed = []
        parsed_old = []

        for line in csvFile:
            parsed_old.append(line)
            separated = line.split(",")
            parsed.append(separated)

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
    
        newCsv = []
        for line in parsed:
            l = ','.join(line)
            newCsv.append(l)


    
        #print(newCsv)

        csvFile.close()

        #save new csv
        newCSVfile = open(outputFolder + ".csv", "w+")

        for line in parsed_old:
            newCSVfile.write("%s" % line)

        newCsv.pop(0)
        newCsv.pop(0)
        for line in newCsv:
            newCSVfile.write("%s" % line)





    e_t = time()

    print("Done.")
    print("Time used: " + str(e_t - s_t))
    print("Images processed: " + str(len(images)))