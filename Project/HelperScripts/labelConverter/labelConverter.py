import numpy as np

# paths of input files
inputCSVPath_phase01 = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase01_csv\trainingSet_phase01.csv'
inputCSVPath_phase02 = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase02_csv\trainingSet_phase02.csv'
inputCSVPath_phase03 = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase03_csv\trainingSet_phase03.csv'

# last item of interest in phase 3 labels
cPh03LastItem = 12
# last item of interest in phase 1 labels
cPh01LastItem = 4

# eye image dimensions
# (width, height)
cEyeImageShape = (100, 100)
# frame dimensions
# (width, height)
cFrameShape = (640, 480)

# face height to width ratio
# constant ratio of face to width (2:3)
cFaceWidthHeightRatio = 1.5
# eye width in respect to face width percentage
cEyeWidthPercentage = 0.3
# eye height in respect to face height percentage
cEyeHeightPercentage = 0.2

# indexes of eyes data in face elements prediction array
cNoLeftEye = 1
cNoRightEye = 2
cLeftEyeX = 3
cLeftEyeY = 4
cRightEyeX = 5
cRightEyeY = 6

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
        for i in range(len(line)):
            if i != 1:
                for j in range(len(line[i])):
                    if i > 1 and j == 0:
                        continue
                    l = l + str(line[i][j]) + ','

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
                        
        #if only one eye found append second one as ones
        if(len(l) == 3):
            temp = [1] * len(l[2])
            l.append(temp)
        if (len(l) > 2):
            result.append(l)

    return result

def datasetCastToFloat(labels):

    for i in range(2, len(labels)):
        for j in range(1, len(labels[i])):
            labels[i][j] = float(labels[i][j])

# filter for only those labels that are of interest
def filterPhaseOneLabels(labels):

    print("[*] Filtering labels of interest in phase 1 ...")

    for i in range(len(labels)):
        l = labels[i]
        l = l[:cPh01LastItem]
        l.append(labels[i][-1])
        labels[i] = l

    return labels

# filter for only those labels that are of interest
def filterPhaseThreeLabels(labels):

    print("[*] Filtering labels of interest in phase 3 ...")

    for i in range(len(labels)):
        l = labels[i]
        l = l[:cPh03LastItem]
        labels[i] = l

    return labels

# translation from phase 3 coordinate system to phase 1 coordinate system
def translatePhaseThreeToPhaseOne(commonLabels):

    print("[*] Translating phase 3 labels to phase 1 ...")

    frameWidth = cFrameShape[0]
    frameHeight = cFrameShape[1]

    for i in range(len(commonLabels)):
        #for j in range(len(commonLabels[i])):
        faceW = commonLabels[i][0][-1]
        faceX = commonLabels[i][0][2]
        faceY = commonLabels[i][0][3]

        # calculate points for face bounding rectangle
        topLeftX = faceX - int((faceW / 2) + 0.5)
        topLeftY = faceY - int(((faceW / 2) * cFaceWidthHeightRatio) + 0.5)

        bottomRightX = faceX + int((faceW / 2) + 0.5)
        bottomRightY = faceY + int(((faceW / 2) * cFaceWidthHeightRatio) + 0.5)

        # calculate eye points of interest on faceImg
        topELeftX, topELeftY = eyeCropPoints(commonLabels[i][1][cLeftEyeX], commonLabels[i][1][cLeftEyeY], faceW)[0]
        topERightX, topERightY = eyeCropPoints(commonLabels[i][1][cRightEyeX], commonLabels[i][1][cRightEyeY], faceW)[0]
 
        # calculate face elements coordinates on face image
        # in respect to whole image
        for k in range(3, len(commonLabels[i][1]) - 1, 2):
            commonLabels[i][1][k] += topLeftX
            commonLabels[i][1][k + 1] += topLeftY

        # calculate eyes points of interest on original frame
        for k in range(2, len(commonLabels[i][2]), 2):
            commonLabels[i][2][k] += (commonLabels[i][1][3] + topELeftX)
            commonLabels[i][2][k + 1] += (commonLabels[i][1][4] + topELeftY)

        for k in range(2, len(commonLabels[i][3]), 2):
            commonLabels[i][3][k] += (commonLabels[i][1][3] + topERightX)
            commonLabels[i][3][k + 1] += (commonLabels[i][1][4] + topERightY)

# x - coordinate of eye centre
# y - coordinate of eye centre
def eyeCropPoints(x, y, faceW):
    # calculate coordinates to crop from
    height, width = faceW * cFaceWidthHeightRatio, faceW
    
    tlEyeX = x - int(cEyeWidthPercentage / 2 * width)
    tlEyeY = y - int(cEyeHeightPercentage / 2 * height)
    brEyeX = x + int(cEyeWidthPercentage / 2 * width)
    brEyeY = y + int(cEyeHeightPercentage / 2 * height)

    return [(tlEyeX, tlEyeY), (brEyeX, brEyeY)]

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

    # filter for labels of interest in phase 1
    filterPhaseOneLabels(phase01_labels)

    # filter for labels of interest in phase 3
    phase03_labels = filterPhaseThreeLabels(phase03_labels)

    # cast all labels to float
    datasetCastToFloat(phase01_labels)
    datasetCastToFloat(phase02_labels)
    datasetCastToFloat(phase03_labels)

    common_labels = []
    common_labels = findCommonLabels(phase01_labels, phase02_labels, phase03_labels)

    #common_labels = [[['capture_2020_04_17_11_39_49_7263', 0.0, 350.0, 331.0, 154.0], ['capture_2020_04_17_11_39_49_7263', 0.0, 0.0, 52.0, 141.0, 144.0, 139.0, 99.0, 173.0, 97.0, 216.0, 97.0, 230.0, 0.0, 0.0, 0.0, 0.0, 200.0], ['capture_2020_04_17_11_39_49_7263_left', 0.0, 50.0, 40.0, 51.0, 56.0, 51.0, 73.0, 18.0, 61.0, 88.0, 56.0], ['capture_2020_04_17_11_39_49_7263_right', 0.0, 54.0, 36.0, 53.0, 51.0, 56.0, 70.0, 24.0, 53.0, 93.0, 55.0]]]

    print(common_labels)

    # translate label coordinates from phase 3 to phase 1 
    translatePhaseThreeToPhaseOne(common_labels)

    # save output labels
    saveCSV(r'C:\Users\arsic\Desktop\master\Rad\output.csv', common_labels)