import os 
import argparse
from pathlib import Path
import numpy as np

fileDir = ""
cmpDir = ""

def argParser():

    global fileDir
    global cmpDir


    retVal = ""

    argsOK = True

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_dir", help = "Directory with whole images", required = True)
    parser.add_argument("-c", "--cmp_dir", help = "Directory with images to delete", required = True)
    args = vars(parser.parse_args())

    try:

        if(len(args["file_dir"]) and len(args["cmp_dir"])):
            fileDir = args["file_dir"]
            cmpDir = args["cmp_dir"]
        else:
            argsOK = False

    except SystemExit as e:
        if e.code != ARG_ERR:
            raise
        else:
            os._exit(ARG_ERR)

    return retVal

def listDirectories():
    p = Path(fileDir).glob('*.jpg')
    filePaths = [x for x in p if x.is_file()]

    for i in range(len(filePaths)):
        filePaths[i] = filePaths[i].name
    

    p = Path(cmpDir).glob('*.jpg')
    cmpPaths = [x for x in p if x.is_file()]
    for i in range(len(cmpPaths)):
        cmpPaths[i] = cmpPaths[i].name


    return [filePaths, cmpPaths]

def diff(A, B):
   return (list(set(A) - set(B))) 
    
if __name__ == "__main__":

    argParser()

    [filePaths, cmpPaths] = listDirectories()
    
    c = diff(filePaths, cmpPaths)

    for i in range(len(c)):
        c[i] = os.path.join(fileDir, c[i])

    for item in c:
        os.remove(item)

    print("Removed: " + str(len(c)) + " items.")
