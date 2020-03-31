import argparse
import sys
import os
import cv2
import datetime
import numpy as np

windowName = "Video source"
startTrackbarName = "Capture (STOP/START):"
keyframesTrackbarName = "Capture FPS: "

outputDirNamebase = "output_"
outputImageNamebase = "capture_"

workingDirPath = os.path.dirname(os.path.realpath(__file__))
outputDirCount = 0

vSourceHelp = "Video source (0 - Internal camera, 1 - External camera, <path>\*.mp4)"

def startCapture(val):
    if(val == 1):
        print("Capture started.")
    else:
        print("Capture stopped.")

def keyframesTracker(val):
    pass

def frameCapture(vsource):

    if(isinstance(vsource, int)):
        cap = cv2.VideoCapture(vsource + cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(vsource)

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if(cap.isOpened() == False):
        print("Error opening video source")

    # frame number
    frameId = 0

    

    # create window and trackbar for starting/stopping capture process
    cv2.namedWindow(windowName)
    cv2.createTrackbar(startTrackbarName, windowName, 0, 1, startCapture)
    cv2.createTrackbar(keyframesTrackbarName, windowName, 1, 30, keyframesTracker)

    dirCreated = False

    outputImageName = outputImageNamebase + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    while(cap.isOpened()):  
        
        if (not dirCreated):
            # count output directories
            countOutputDirs()

            # make new directory
            # as for not to override the previous one
            outputDirName = createNewOutputDir()

            dirCreated = True

        ret, frame = cap.read();
        
        # frames of interest
        keyframesPerSec = cv2.getTrackbarPos(keyframesTrackbarName, windowName)

        if(keyframesPerSec == 0):
            keyframesPerSec = 1

        if(ret == True):
            cv2.imshow(windowName, frame)
            
            if(cv2.getTrackbarPos(startTrackbarName, windowName)):
                if(frameId % keyframesPerSec == 0):
                    cv2.imwrite(os.path.join(workingDirPath, outputDirName, outputImageName + "_{:d}.jpg").format(frameId), frame)
            frameId += 1
            
            if(cv2.waitKey(25) & 0xFF == ord('q')):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def countOutputDirs():
    global outputDirCount 
    outputDirCount = int(len(next(os.walk(workingDirPath))[1]))
    print("Output directories: " + str(outputDirCount))

def createNewOutputDir():
    global outputDirCount

    outputDirCount += 1
    outputDirName = outputDirNamebase + str(outputDirCount)
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    return outputDirName

def main():

    videoSource = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vsource", help = vSourceHelp, required = True)

    args = vars(parser.parse_args())

    if (args["vsource"] == '0' or args["vsource"] == '1'):
        videoSource = int(args["vsource"])
    elif (len(args["vsource"]) > 1):
        videoSource = args["vsource"]
    else:
        print("Usage: ImageCapture.py -v <videosource>")
        sys.exit(2)

    print("Video source: ", videoSource)

    print(workingDirPath)
    print(os.path.join(workingDirPath, "output"))
    frameCapture(videoSource)

if __name__ == "__main__":
   main()
