import numpy as np

faceElementsPath = 'C:\\Users\\Cisra\\Desktop\\faces49_normalized.csv'

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
	
def readFaceElementsFromCSV(filepath):
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
				cat[cnt_cat] = float(item)
				cnt_cat = cnt_cat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result
	
def denormalizeFaceElements(elements):
	result = []
	
	for arr in elements:
		cnt = 0
		tempArr = []
		
		for cnt in range(0, 22, 2):
			tempX = arr[cnt] * arr[len(arr) - 1]
			tempY = arr[cnt + 1] * (arr[len(arr) - 1] * 1.5)
			tempArr.append(tempX)
			tempArr.append(tempY)
			
		tempArr = np.ceil(np.asarray(tempArr))
		result.append(tempArr)
					
	return result
	
def readLookAngle(elements):
	result = []
	
	for arr in elements:
		cnt = 0
		tempArr = []
		
		for cnt in range(22, 26):
			tempArr.append(arr[cnt])
			
		result.append(tempArr)
	
	return result


result = []
result = readFaceElementsFromCSV(faceElementsPath)

faceElementsDenom = []
faceElementsDenom = denormalizeFaceElements(result)

lookAngle = []
lookAngle = readLookAngle(result)

print(result)
print(faceElementsDenom)
print(lookAngle)