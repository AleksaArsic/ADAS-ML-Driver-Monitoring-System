import numpy as np

# paths of input files
inputCSVPath_phase01 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase01_csv\\trainingSet_phase01.csv'
inputCSVPath_phase02 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase02_csv\\trainingSet_phase02.csv'
inputCSVPath_phase03 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase03_csv\\trainingSet_phase03.csv'

# last item of interest in phase 3 labels
cPh03LastItem = 12

# eye image dimensions
# (width, height)
cEyeImageShape = (100, 100)
# frame dimensions
# (width, height)
cFrameShape = (640, 480)

# face height to width ratio
cFaceHeigthToWidthRation = 1.5
# eye width in respect to face width percentage
cEyeWidthPercentage = 0.3
# eye height in respect to face height percentage
cEyeHeightPercentage = 0.2

# read CSV file
def readCSV(filepath):

    print("[*] Loading labels: " + str(filepath.split('\\')[-1]))

    result = []
    dat_file = open(filepath,'r')
    lines=dat_file.readlines()

    for line in lines:
        if len(line)>0:
            l = line.split(',')
            l[-1] = l[-1][:-1]
            result.append(l)
    return result

# save csv file
def saveCSV(filepath, labels):

    print("[*] Saving labels: " + str(filepath.split('\\')[-1]))

    dat_file = open(filepath, "w+")

    for line in labels:
        l = ''
        for item in line:
            l = l + str(item) + ','

        l = l + '\n'
        dat_file.write(str(l))


    dat_file.close()

# find common labels among two labeled datasets
# find based on common image name
def findCommonLabels(labels1, labels2, labels3):

    print("[*] Finding common label names ...")

    result = []

    for i in range(2, len(labels1)):
        l = []
        l.append(labels1[i])
        for j in range(2, len(labels2)):
            if (labels1[i][0] in labels2[j][0]):
                l.append(labels2[j])
                for k in range(2, len(labels3)):
                    if(labels2[j][0] in labels3[k][0]):
                        l.append(labels3[k])
                        
        
        if (len(l) > 2):
            result.append(l)

    return result

# filter for only those labels that are of interest
def filterPhaseThreeLabels(labels):

    print("[*] Filtering labels of interest in phase 3 ...")

    for i in range(len(labels)):
        l = labels[i]
        l = l[:cPh03LastItem]
        labels[i] = l

    return labels

# TO-DO: implement functionality that will assure safe
# translation from phase 3 coordinate system to phase 1 coordinate system
def translatePhaseThreeToPhaseOne(commonLabels):

    print("[*] Translating phase 3 labels to phase 1 ...")

    frameWidth = cFrameShape[0]
    frameHeight = cFrameShape[1]

    for i in range(len(commonLabels)):
        for j in range(len(commonLabels[i])):
            faceW = commonLabels[i][j][-1]
            faceX = commonLabels[i][j][2]
            faceY = commonLabels[i][j][3]

            #eyeWidth = cEyeWidthPercentage * float(faceWidth)
            #eyeHeight = cEyeHeightPercentage * faceHeight

            # calculate points for face bounding rectangle
            topLeftX = faceX - int((faceW / 2) + 0.5)
            topLeftY = faceY - int(((faceW / 2) * cFaceWidthHeightRatio) + 0.5)

            bottomRightX = faceX + int((faceW / 2) + 0.5)
            bottomRightY = faceY + int(((faceW / 2) * cFaceWidthHeightRatio) + 0.5)

            # calculate eye points of interest on faceImg
            topELeftX, topELeftY = eyeCropPoints(faceElementsPrediction[cLeftEyeX], faceElementsPrediction[cLeftEyeY])[0]
            topERightX, topERightY = eyeCropPoints(faceElementsPrediction[cRightEyeX], faceElementsPrediction[cRightEyeY])[0]
  

def eyeCropPoints(x, y, faceW):
    # calculate coordinates to crop from
    height, width = faceW * cFaceHeigthToWidthRation, faceW
    
    tlEyeX = x - int(cEyeWidthPercentage / 2 * width)
    tlEyeY = y - int(cEyeHeightPercentage / 2 * height)
    brEyeX = x + int(cEyeWidthPercentage / 2 * width)
    brEyeY = y + int(cEyeHeightPercentage / 2 * height)

    return [(tlEyeX, tlEyeY), (brEyeX, brEyeY)]

# draws all predictions on original image
def drawPredictionOnImage(facePrediction, faceElementsPrediction, eyesPrediction):

    # denormalize face predictions
    #[faceXDenom, faceYDenom, faceWDenom] = denormalizeFacePrediction(facePrediction)

    # calculate points for face bounding rectangle to be drawn
    topLeftX = faceXDenom - int((faceWDenom / 2) + 0.5)
    topLeftY = faceYDenom - int(((faceWDenom / 2) * cFaceWidthHeightRatio) + 0.5)

    bottomRightX = faceXDenom + int((faceWDenom / 2) + 0.5)
    bottomRightY = faceYDenom + int(((faceWDenom / 2) * cFaceWidthHeightRatio) + 0.5)

    # denormalize face elements to a new array
    #faceElementsPredDenorm = denormalizeFaceElementsPrediction(faceElementsPrediction, resizeFactor = cLabeledFaceHeight / faceImg.shape[0])[0]
    
    # denormalize eyes points of interest
    # faceWDenom * cEyeWidthPerc because eye dimension is 30% of faceWDenom
    #if len(eyesPrediction) and faceElementsPrediction[0][cNoLeftEye] < cNoEyeThreshold:
    #    leftEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataLeft], faceWDenom * cEyeWidthPerc, 1, 11)
    #if len(eyesPrediction) and faceElementsPrediction[0][cNoRightEye] < cNoEyeThreshold:
    #    rightEyePredDenorm = denormalizeEyesPrediction(eyesPrediction[cEyesDataRight], faceWDenom * cEyeWidthPerc, 1, 11)

    # calculate eye points of interest on faceImg
    topELeftX, topELeftY = eyeCropPoints(faceElementsPrediction[cLeftEyeX], faceElementsPrediction[cLeftEyeY])[0]
    topERightX, topERightY = eyeCropPoints(faceElementsPrediction[cRightEyeX], faceElementsPrediction[cRightEyeY])[0]
  
    # calculate face elements coordinates on face image
    for i in range(0, len(faceElementsPredDenorm), 2):
        faceElementsPrediction[i] += topLeftX
        faceElementsPrediction[i + 1] += topLeftY

    # calculate eyes points of interest on original frame
    for i in range(1, len(leftEyePredDenorm) - 5, 2):
        leftEyePredDenorm[i] += (faceElementsPredDenorm[0] + topELeftX)
        leftEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topELeftY)

    for i in range(1, len(rightEyePredDenorm) - 5, 2):
        rightEyePredDenorm[i] += (faceElementsPredDenorm[0] + topERightX)
        rightEyePredDenorm[i + 1] += (faceElementsPredDenorm[1] + topERightY)


# translated phase 3 labels to labels from phase 1
def formatOutputLabels(commonLabels):

    print("[*] Formating output labels ...")
    
    result = []

    for list in commonLabels:
        l2 = list[1][1:]
        result.append(list[0] + l2)

    return result

if __name__ == "__main__":

    print("######################################################")
    print("#                 Label converter                    #")
    print("######################################################")

    # load phase 1 labels
    phase01_labels = []
    phase01_labels = readCSV(inputCSVPath_phase01)

    # load phase 2 labels
    phase02_labels = []
    phase02_labels = readCSV(inputCSVPath_phase02)

    # load phase 3 labels
    phase03_labels = []
    phase03_labels = readCSV(inputCSVPath_phase03)

    # filter for labels of interest in phase 3
    phase03_labels = filterPhaseThreeLabels(phase03_labels)

    # find common labels in datasets
    #common_labels_ph12 = []
    #common_labels_ph12 = findCommonLabels(phase01_labels, phase02_labels)

    common_labels = []
    common_labels = findCommonLabels(phase01_labels, phase02_labels, phase03_labels)

    print(len(common_labels))

    # format output labels
    common_labels = formatOutputLabels(common_labels)

    # translate label coordinates from phase 3 to phase 1 
    #translatePhaseThreeToPhaseOne(common_labels)

    # save output labels
    saveCSV('C:\\Users\\Cisra\\Desktop\\Rad\\output.csv', common_labels)