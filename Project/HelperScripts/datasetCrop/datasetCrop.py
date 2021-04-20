import os 
import glob 
import sys
import shutil

# dataset path
datasetPath = r'C:\Users\arsic\Desktop\master\Rad\CNN-Driver-Monitoring-System\Dataset\trainingSet_phase01'
# dataset .csv path
datasetCSVPath = r'C:\Users\arsic\Desktop\master\Rad\output.csv'
# output dataset path
outputPath = r'C:\Users\arsic\Desktop\master\Rad\output'


# used for reading whole .csv files
def parseFileNamesFromCSV(filepath):
    result = []
    datFile = open(filepath,'r')
    lines=datFile.readlines()
    for line in lines:
        if len(line)>0:
            p1 = line.find(',')
            filename = line[0:p1]
            result.append(filename)
    return result

def cropDataset(datasetPath, imageNames, outputPath):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    else:
        shutil.rmtree(outputPath)
        os.makedirs(outputPath)

    # find photos of interest and copy them to output folder
    for file in imageNames:
        imagePath = datasetPath + '\\' + file + '.jpg'
        shutil.copy(imagePath, outputPath)

if __name__ == "__main__":

    imageNames = parseFileNamesFromCSV(datasetCSVPath)

    cropDataset(datasetPath, imageNames, outputPath)