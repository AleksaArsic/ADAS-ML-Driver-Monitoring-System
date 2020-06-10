import numpy as np

minMaxCSVpath = 'D:\\Diplomski\\DriverMonitoringSystem\\Dataset\\output_2020_04_17_11_39_49_faceMode_min_max.csv'

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

def readMinMaxFromCSV(filepath):
	
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
				cat[cnt_cat] = int(item)
				cnt_cat = cnt_cat + 1
			cat = np.asarray(cat)
			
			result.append(cat)

	return result
	
result = []
result = readMinMaxFromCSV(minMaxCSVpath)

print(result)