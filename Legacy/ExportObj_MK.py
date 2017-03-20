import os
import math
import itertools
import time

doc = PhotoScan.app.document
count = 1 

for _CurrentChunk in doc.chunks:

    ###gets folder containing chunk pics/source folder instead of building it
    path_Pic = _CurrentChunk.cameras[0].photo.path
    picName = path_Pic.split("/")[-1]
    folderPic = path_Pic.rstrip(picName)

    ###naming the file
    folder = folderPic
    name = _CurrentChunk.label
    file = name 
    fullFilePath = folder + file +".obj"




    ###exporting file as obj


    if os.path.exists(folder):
        if os.path.isfile(fullFilePath):
            print("This file already exists:  " + fullFilePath)
            continue
        message1 = "Attempting to export:".rjust(150)
        message2 = fullFilePath.rjust(150)
        message = message1 + "\n" + message2
        print(message)

        _CurrentChunk.exportModel(fullFilePath)
        #time.sleep(140)
        

        #_CurrentChunk.exportModel(fullFilePath, binary=False, precision=6, texture_format="jpg", texture=True, normals=True, colors=True, cameras=False, udim=False, strip_extensions=True)

        print("\n")
        count += 1



    else:
        message = "Failed to export: " + fullFilePath
        print(message)
        print("\n")



    #doc.save()


    #V:\Projects\Woolworth Building\Field Survey\Dormer Survey\AGI Renders\N04-43-TB-TRANSITION AT TURRET
    #V:/Projects/Woolworth Building/Field Survey/Dormer Survey/AGI Renders/N04-43-TB-TRANSITION AT TURRET/N04-43-TB-TRANSITION AT TURRET.obj









