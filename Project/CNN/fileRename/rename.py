import os 
from pathlib import Path

dirpath = 'C:\\Users\\arsic\\Desktop\\Diplomski\\DriverMonitoringSystem\\Project\\CNN\\CNN\\CNN\\false_2020_06_09_09_37_23'

paths = sorted(Path(dirpath).iterdir(), key = os.path.getmtime)

print(paths)

for i in range(len(paths)):
    old_path = str(paths[i])
    paths[i] = '_'.join(str(paths[i]).split('_')[:-1])
    paths[i] = (paths[i] + "_{0:0=6d}.jpg").format(i)
    os.rename(old_path, paths[i])
    
print(paths)


#outputName = os.path.join("", outputImageName + "_{0:0=6d}.jpg").format(i)
