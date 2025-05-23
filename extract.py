import os
import shutil

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if fullPath.endswith('.webp'):
                allFiles.append(fullPath)
    return allFiles

# Paths
dirname = r'E:\Python_projects\New folder\filtered_data'  # Source directory
dest = r"E:\Python_projects\New folder\gif_extract\gif_data"  # Destination directory

# Ensure the destination directory exists
os.makedirs(dest, exist_ok=True)

# Get list of .webp files and copy them
data = getListOfFiles(dirname)
for i in range(len(data)):
    fname = os.path.join(dest, f"{i}.webp")  # Join the destination path with new file name
    shutil.copyfile(data[i], fname)
