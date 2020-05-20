import argparse
import sys
import os
import cv2
import datetime
import numpy as np

ARG_ERR = 255

# resolution of output captures
captureWidth = 640
captureHeight = 480

windowName = "Video source"
startTrackbarName = "Capture (STOP/START):"
keyframesTrackbarName = "Capture FPS: "

# maximal number of frames that we want to capture in one second
keyframesTrackbarMax = 30

outputDirNamebase = "output_"
outputImageNamebase = "capture_"

workingDirPath = os.path.dirname(os.path.realpath(__file__))
outputDirCount = 0

vSourceHelp = "Video source (0 - Internal camera, 1 - External camera, <path>\*.mp4)"
outputWidthHelp = "Width of the output capture"
outputHeightHelp = "Height of the output capture"

def startCapture(val):
    if(val == 1):
        print("Capture started.")
    else:
        print("Capture stopped.")

def keyframesTracker(val):
    pass

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def frameCapture(vsource):

    resizeVideoFrame = False

    if(isinstance(vsource, int)):
        cap = cv2.VideoCapture(vsource + cv2.CAP_DSHOW)
        change_res(cap, captureWidth, captureHeight)
    else:
        cap = cv2.VideoCapture(vsource)
        resizeVideoFrame = True

    if(cap.isOpened() == False):
        print("Error opening video source")

    # frame number
    frameId = 0

    # create window and trackbar for starting/stopping capture process
    cv2.namedWindow(windowName)
    cv2.createTrackbar(startTrackbarName, windowName, 0, 1, startCapture)
    # create trackbar for how many frapes per second we want to capture
    cv2.createTrackbar(keyframesTrackbarName, windowName, 1, keyframesTrackbarMax, keyframesTracker)

    dirCreated = False

    dateTimeNow = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    outputImageName = outputImageNamebase + dateTimeNow

    while(cap.isOpened()):  
        
        if (not dirCreated):
            # count output directories
            countOutputDirs()

            # make new directory
            # as for not to override the previous one
            outputDirName = createNewOutputDir(dateTimeNow)

            dirCreated = True

        ret, frame = cap.read();
        
        if (resizeVideoFrame):
            frame = image_resize(frame, captureWidth, captureHeight)

        # frames of interest
        keyframesPerSec = keyframesTrackbarMax - cv2.getTrackbarPos(keyframesTrackbarName, windowName)

        if(keyframesPerSec == 0):
            keyframesPerSec = 1

        if(ret == True):
            cv2.imshow(windowName, frame)
            
            if(cv2.getTrackbarPos(startTrackbarName, windowName)):
                if(frameId % keyframesPerSec == 0):
                    cv2.imwrite(os.path.join(workingDirPath, outputDirName, outputImageName + "_{:d}.jpg").format(frameId), frame)
            frameId += 1
            
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def countOutputDirs():
    global outputDirCount 
    outputDirCount = int(len(next(os.walk(workingDirPath))[1]))
    print("Output directories: " + str(outputDirCount))

def createNewOutputDir(dateTimeNow):

    outputDirName = outputDirNamebase + dateTimeNow
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    return outputDirName

def argParser():
    global captureWidth
    global captureHeight

    argsOK = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vsource", help = vSourceHelp, required = True)
    parser.add_argument("-ow", "--out_width", help = outputWidthHelp, required = False)
    parser.add_argument("-oh", "--out_height", help = outputHeightHelp, required = False)

    args = vars(parser.parse_args())

    try:
        if (args["vsource"] == '0' or args["vsource"] == '1'):
            videoSource = int(args["vsource"])
        elif (len(args["vsource"]) > 1):
            videoSource = args["vsource"]
        else:
            argsOK = False;

        if args["out_width"] is not None or args["out_height"] is not None:
            argsOK = True
            #else:
            if(len(args["out_width"])):
                captureWidth = int(args["out_width"])
            else:
                argsOK = False
            if(len(args["out_height"])):
                captureHeight = int(args["out_height"])
            else:
                argsOK = False

        if not argsOK:
            print("Usage: ImageCapture.py -v <videosource> [-ow <out_width>, -oh <out_height>]")
            sys.exit(ARG_ERR)

    except SystemExit as e:
        if e.code != ARG_ERR:
            raise
        else:
            os._exit(ARG_ERR)

    return videoSource

def main():

    videoSource = argParser()
   
    print("Video source: ", videoSource)

    print(workingDirPath)
    print(os.path.join(workingDirPath, "output"))
    frameCapture(videoSource)

if __name__ == "__main__":
   main()
