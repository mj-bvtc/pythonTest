import os
import math
import itertools
import time



def exportObj(_CurrentChunk):

    doc = PhotoScan.app.document
    ###gets folder containing chunk pics/source folder instead of building it
    path_Pic = _CurrentChunk.cameras[0].photo.path
    picName = path_Pic.split("/")[-1]
    folderPic = path_Pic.rstrip(picName)

    ###naming the file
    folder = folderPic
    label = _CurrentChunk.label
    newPath = "C:\\Users\\peters\\Desktop\\"
    name = str(label).replace("-", "_")
    fullFilePath = ""
    fullFilePath = folder + name +".obj"

    
    if os.path.exists(folder):

        message1 = "Attempting to export:".rjust(150)
        message2 = fullFilePath.rjust(150)
        message = message1 + "\n" + message2
        print(message)

        _CurrentChunk.exportModel(fullFilePath)
        #time.sleep(20)
        

        #_CurrentChunk.exportModel(fullFilePath, binary=False, precision=6, texture_format="jpg", texture=True, normals=True, colors=True, cameras=False, udim=False, strip_extensions=True)

        print("\n")




    else:
        message = "Failed to export: " + fullFilePath
        print(message)
        print("\n")

def exportObjLoop(overwrite = False):
    doc = PhotoScan.app.document

    for _CurrentChunk in doc.chunks:


        ###gets folder containing chunk pics/source folder instead of building it
        path_Pic = _CurrentChunk.cameras[0].photo.path
        picName = path_Pic.split("/")[-1]
        folderPic = path_Pic.rstrip(picName)

        ###naming the file
        folder = folderPic
        label = _CurrentChunk.label
        newPath = "C:\\Users\\peters\\Desktop\\"
        name = str(label).replace("-", "_")
        fullFilePath = ""
        fullFilePath = folder + name +".obj"

        if os.path.isfile(fullFilePath):
            print("This file already exists:  " + fullFilePath)
            if overwrite == True:
                print("\tOverwriting existing file:  " + fullFilePath)
                exportObj(_CurrentChunk)
            else: 
                print("\tNo action taken on:  " + fullFilePath)
                continue
        else:
            print("Writing new file: " + fullFilePath)

            exportObj(_CurrentChunk)

exportObjLoop(overwrite = False)










