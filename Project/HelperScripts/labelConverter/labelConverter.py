import numpy as np

# paths of input files
inputCSVPath_phase01 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase01_csv\\trainingSet_phase01.csv'
inputCSVPath_phase03 = 'C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase03_csv\\trainingSet_phase03.csv'

# read CSV file
def readCSV(filepath):
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
    result = []

    k = 0
    for i in range(2, len(labels1)):
        for j in range(2, len(labels2)):
            if (labels1[i][0] in labels2[j][0]):
                result.append([labels1[i], labels2[j]])
                continue

    return result

# TO-DO: filter needed labels from phase 3 dataset
def filterPhaseThreeLabels(labels):
    pass

# TO-DO: implement functionality that will assure safe
# translation from phase 3 coordinate system to phase 1 coordinate system
def translatePhaseThreeToPhaseOne(labels1, labels2):
    pass

if __name__ == "__main__":

    # load phase 1 labels
    phase01_labels = []
    phase01_labels = readCSV(inputCSVPath_phase01)

    # load phase 3 labels
    phase03_labels = []
    phase03_labels = readCSV(inputCSVPath_phase03)

    # find common labels in datasets
    common_labels = []
    common_labels = findCommonLabels(phase01_labels, phase03_labels)

    saveCSV('C:\\Users\\Cisra\\Desktop\\Rad\\trainingSet_phase01_csv\\trainingSet_phase01_copy.csv', phase01_labels)