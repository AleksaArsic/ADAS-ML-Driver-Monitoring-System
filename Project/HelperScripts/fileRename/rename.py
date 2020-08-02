import os 
from pathlib import Path

dirpath = 'D:\\ImageCapture\\ImageCapture\\output_2020_08_01_22_19_42\\'

paths = sorted(Path(dirpath).iterdir(), key = os.path.getmtime)

print(paths)

for i in range(len(paths)):
    old_path = str(paths[i])
    paths[i] = '_'.join(str(paths[i]).split('_')[:-2])
    paths[i] = (paths[i] + "_{0:0=6d}.jpg").format(i + 50000)
    os.rename(old_path, paths[i])
    
print(paths)
