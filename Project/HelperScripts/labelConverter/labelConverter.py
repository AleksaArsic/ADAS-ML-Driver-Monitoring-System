import numpy as np

# paths of input files
inputCSVPath_phase01 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase01_csv\\trainingSet_phase01.csv'
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
def findCommonLabels(labels1, labels2):

    print("[*] Finding common label names ...")

    result = []

    k = 0
    for i in range(2, len(labels1)):
        for j in range(2, len(labels2)):
            if (labels1[i][0] in labels2[j][0]):
                result.append([labels1[i], labels2[j]])
                continue

    return result

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
            faceWidth = commonLabels[i][j][-1]
            faceHeight = cFaceHeigthToWidthRation * float(faceWidth)

            eyeWidth = cEyeWidthPercentage * float(faceWidth)
            eyeHeight = cEyeHeightPercentage * faceHeight

            # idea: we have precentages and dimensions so we can easly manipulate numbers
            # and coordinates to match phase 2 and at last phase 1
            # idea is to scale coordinates systems of phase 3 and phase 2 
            # by using those percentages and dimnesions

# TO-DO: implement functionality that will concatenate
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

    # load phase 3 labels
    phase03_labels = []
    phase03_labels = readCSV(inputCSVPath_phase03)

    # filter for labels of interest in phase 3
    phase03_labels = filterPhaseThreeLabels(phase03_labels)

    # find common labels in datasets
    common_labels = []
    common_labels = findCommonLabels(phase01_labels, phase03_labels)

    # format output labels
    common_labels = formatOutputLabels(common_labels)

    # translate label coordinates from phase 3 to phase 1 
    #translatePhaseThreeToPhaseOne(common_labels)

    # save output labels
    saveCSV('C:\\Users\\Cisra\\Desktop\\Rad\\output.csv', common_labels)