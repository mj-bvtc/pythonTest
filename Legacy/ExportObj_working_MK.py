import os
import math
import itertools
import time

doc = PhotoScan.app.document

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
    #name1 = str(label).replace("-", "_")
    name = str(label).replace(" ","_")

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

        if isModel(_CurrentChunk) == False:
            continue

        doc = PhotoScan.app.document
        ###gets folder containing chunk pics/source folder instead of building it
        path_Pic = _CurrentChunk.cameras[0].photo.path
        picName = path_Pic.split("/")[-1]
        folderPic = path_Pic.rstrip(picName)

        ###naming the file
        folder = folderPic
        label = _CurrentChunk.label
        newPath = "C:\\Users\\peters\\Desktop\\"
        #name1 = str(label).replace("-", "_") ###Uneccessary, used in troubleshooting
        name = str(label).replace(" ","_") ###spaces in fileName break model from texture, this changes spaces to "_"

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

def isModel(_CurrentChunk):
    if _CurrentChunk.model:
        print("This model exists:  " + _CurrentChunk.label)
        return True
    else:
        indent = "\t"
        indent *= 15
        messageContents = indent + "This model DOES NOT exist:  " + _CurrentChunk.label
        message = messageContents
        print(message)
        return False

exportObjLoop(overwrite = False)













