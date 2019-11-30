import os

# List all files in a directory using os.listdir
basepath = './inputFiles/'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)
        fileFullName=basepath+entry
        f = open(fileFullName, "r")
        print("******* content of file "+fileFullName+"  ****************")
        for x in f:
            print(x)
