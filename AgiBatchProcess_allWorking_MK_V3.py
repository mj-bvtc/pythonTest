import PhotoScan
import os
import math
import itertools

doc = PhotoScan.app.document

def chunkExists(_CurrentChunk):
    if not _CurrentChunk:
        print("Error: chunk is none")
        return False
    else:
        print("Chunk exists")
        return True

def chunkEnabled(_CurrentChunk):
    if not _CurrentChunk.enabled:
        print("Error: chunk is not enabled, skipping")
        return False
    else:
        print("Chunk enabled")
        return True

def chunkCheck(_CurrentChunk):
    if chunkExists(_CurrentChunk) and chunkEnabled(_CurrentChunk):
        print("It's all good, continuing to process chunk")
        return True
    else:
        return False

def alignment(_CurrentChunk):

    #initial alignment 
    _CurrentChunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection, keypoint_limit=40000, tiepoint_limit=4000)
    _CurrentChunk.alignCameras()
    initialPointCount = len(_CurrentChunk.point_cloud.points)
    print("Original Point initialPointCount: ")
    print(initialPointCount)

def isAligned(_CurrentChunk):
    if _CurrentChunk.point_cloud:
        print("This chunk already has a sparse cloud:  " + _CurrentChunk.label)
        return True
    else:
        print("This chunk does not have a sparse cloud:  " + _CurrentChunk.label)
        return False

def error(_CurrentChunk):

    # Compatibility - Agisoft PhotoScan Professional 1.2.4
    # saves reprojection error for the tie points in the sparse cloud 



    doc = PhotoScan.app.document



    M = _CurrentChunk.transform.matrix
    crs = _CurrentChunk.crs
    point_cloud = _CurrentChunk.point_cloud
    projections = point_cloud.projections
    points = point_cloud.points
    npoints = len(points)
    tracks = point_cloud.tracks




    points_coords = {}
    points_errors = {}
    errorList = []

    for photo in _CurrentChunk.cameras:

        if not photo.transform:
            continue

        T = photo.transform.inv() 
        calib = photo.sensor.calibration
    
        point_index = 0
        for proj in projections[photo]:
            track_id = proj.track_id
            while point_index < npoints and points[point_index].track_id < track_id:
                point_index += 1
            if point_index < npoints and points[point_index].track_id == track_id:
                if points[point_index].valid == False: 
                    continue



                coord = T * points[point_index].coord
                coord.size = 3
                dist = calib.error(coord, proj.coord).norm() ** 2
                v = M * points[point_index].coord
                v.size = 3



                if point_index in points_errors.keys():
                    point_index = int(point_index)
                    points_errors[point_index].x += dist
                    points_errors[point_index].y += 1
                else:
                    points_errors[point_index] = PhotoScan.Vector([dist, 1])

    for point_index in range(npoints):

        if points[point_index].valid == False:
            continue
        
        if _CurrentChunk.crs:
            w = M * points[point_index].coord
            w.size = 3
            X, Y, Z = _CurrentChunk.crs.project(w)
        else:
            X, Y, Z, w = M * points[point_index].coord

        error = math.sqrt(points_errors[point_index].x / points_errors[point_index].y)
        errorList.append(error)
        errorList.sort()






    avgError = sum(errorList)/len(errorList) ###for original photos, no point manipulation recorded

    validPtList = []

    for pt in _CurrentChunk.point_cloud.points: ##Makes a list of points that are NOT deleted 
        if pt.valid == True:
            validPtList.append(pt)
        else:
            continue


    count = 0

    #for err in errorList: ## loops through error values in error list
    #    if err > 1.5*avgError:
    #        validPtList[count].selected = True
    #    count += 1



    print(avgError)
    print(max(errorList))
    return avgError

def lowError(_CurrentChunk):
    #Reduces error without removing too many points, while loop
    ##total_error, ind_error = calc_reprojection(_CurrentChunk)
    ####print(total_error, ind_error)  http://www.agisoft.com/forum/index.php?topic=4514.msg22917#msg22917  ####
    ###################################http://www.agisoft.com/forum/index.php?topic=5267.msg26171#msg26171

    ptList = _CurrentChunk.point_cloud.points
    initialPtCount = len(ptList)
    print("initial points: " + str(initialPtCount))


    #initial settings before loop\
    
    error1 = error(_CurrentChunk)

    initialPts = initialPtCount
    currentPts = initialPts
    count = 0
    while error1 >= 1.000:
        #prints current error as it goes through loop
        print("initial error: " + str(error1))

        #breaks if half points or more removed
        if initialPts*.50 > currentPts:
            print("Percentage of points removed too high, I stopped it")
            break

        tiePtCount = len(_CurrentChunk.point_cloud.points)
        #breaks if less than 40K points are left
        if tiePtCount < 5000:
            print("Point count almost went below 40,000, I stopped it")
            break

        #breaks if loop runs more than 1K times
        if count > 100:
            print("This may have ran forever, I stopped it")
            break

        #optimize camera alignment before removing points
        _CurrentChunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_b1=True, fit_b2=True, fit_k1k2k3=True,fit_p1p2=True, fit_k4=True, fit_p3=True, fit_p4=True)

        #remove error by %, lower point count (for simulation only), advance count by 1
        error1 *= .80
        #currentPts -= 500
        count += 1
        _CurrentChunk.buildPoints(error = (_CurrentChunk.buildPoints(error1)))

    #prints total number of times loop ran
    print("While loop ran " + str(count) + " times")
    print("Number of points after gradual selection: ")
    print(len(_CurrentChunk.point_cloud.points))

def processChunk(_CurrentChunk):

    #Process Chunks after the initial alignment and gradual selection 

    if isDenseCld(_CurrentChunk) == False:
        _CurrentChunk.buildDenseCloud(quality=PhotoScan.HighQuality)
        doc.save()
    
    if isMeshed(_CurrentChunk) == False:
        _CurrentChunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation, face_count = 2000000)
        doc.save()
    if isTextured(_CurrentChunk) == False:
        _CurrentChunk.buildUV(mapping=PhotoScan.GenericMapping)
        _CurrentChunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
        doc.save()

def isDenseCld(_CurrentChunk):
    if _CurrentChunk.dense_cloud:
        print("This chunk already has a dense cloud:  " + _CurrentChunk.label)
        return True
    else:
        print("This chunk does not have a dense cloud:  " + _CurrentChunk.label)
        return False

def isMeshed(_CurrentChunk):
    if _CurrentChunk.model:
        print("This chunk already has a model:  " + _CurrentChunk.label)
        return True
    else:
        print("This chunk does not have a model:  " + _CurrentChunk.label)
        return False

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
                print("Overwriting existing file:  " + fullFilePath)
                exportObj(_CurrentChunk)
            else: 
                print("No action taken on:  " + fullFilePath)
                continue
        else:
            print("Writing new file: " + fullFilePath)

            exportObj(_CurrentChunk)

def isModel(_CurrentChunk):
    if _CurrentChunk.model:
        print("This model exists:  " + _CurrentChunk.label)
        return True
    else:
        message = "This model DOES NOT exist:  " + _CurrentChunk.label
        print(message)
        return False

def ptdist(pta, ptb):
    x = ptb[0]-pta[0]
    y = ptb[1]-pta[1]
    z = ptb[2]-pta[2]
    distance = math.sqrt((x)**2+(y)**2+(z)**2)
    return distance

def midPt(ptA, ptB):
   x = (ptA[0]+ptB[0])/2
   y = (ptA[1]+ptB[1])/2
   z = (ptA[2]+ptB[2])/2
   return [x,y,z]

def cropPtFromCameras(_CurrentChunk):

    pointList = []

    combos = list(itertools.combinations(_CurrentChunk.cameras,2))
    #print(combos)

    camList = []
    for cam in _CurrentChunk.cameras:
        if cam.center != None:

            pointList.append(cam.center)
            camList.append(cam.label)

    #print(pointList)

    ptCombos = list(itertools.combinations(pointList,2))

    #print(ptCombos)


    distList = []

    a = [0,0,0]
    b = [8,0,0]

    testDist = ptdist(a,b)
    #print(testDist)



    for pt in ptCombos:
        
        dist = ptdist(pt[0],pt[1])
        distList.append(dist)
        


    

    maxDist = max(distList) #biggest distance
    print(maxDist)

    index = distList.index(maxDist) #index of biggest distance
    #print(index)

    farPts = ptCombos[index]
    f1 = farPts[0] #Coordinates of far camA
    f2 = farPts[1] #Coordinates of far camA

    camIndA = pointList.index(farPts[0])
    camIndB = pointList.index(farPts[1])

    cam1 = camList[camIndA] #name of farthest cameraA
    cam2 = camList[camIndB] #name of farthest cameraB
    
    tiePts = []
    
    center = midPt(f1,f2) #midpoint between 2 far points, center of selection sphere

    for pt in _CurrentChunk.point_cloud.points:
        tiePts.append(pt.coord)

    selPtList = []

    for pt in _CurrentChunk.point_cloud.points:
        if ptdist(center,pt.coord) < maxDist * 1.15:
            pt.selected = True
            selPtList.append(pt)
        else:
            pt.selected = False

    _CurrentChunk.point_cloud.cropSelectedPoints()
    _CurrentChunk.resetRegion() #Helps gradual selection work only on points of interest
    camCropPtList = len(_CurrentChunk.point_cloud.points)

    print("After cropping points too far from cameras there were: ")
    print(camCropPtList)

    message = cam1 + " and " + cam2 + " are the farthest photos apart from each other.  They are " + str(maxDist) + " units apart from one another."
    message += " They are located at " + str(f1) + " and " + str(f2)
    message += " Halfway between them is " + str(center) + " A selection of nearby points will be made, and those points will be cropped. Thanks, and have a greeeeat day"
    print(message)

def processAllChunks():

    for _CurrentChunk in doc.chunks:

        print(_CurrentChunk.label + ":    starting to process--------------------------------------------------------------------------------")
        if chunkCheck(_CurrentChunk) == False:
            continue
        print(_CurrentChunk.label)
        if isAligned(_CurrentChunk) == False:
            alignment(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            lowError(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)

        ###check if there are way too few points to make good mesh
        minPoints = 2000
        pointsInChunk = len(_CurrentChunk.point_cloud.points)
        name = _CurrentChunk.label
        if pointsInChunk < minPoints:
            print("Less than required number of points to generate good model")
            print("{} required points, {} points in chunk {}  ".format(minPoints, pointsInChunk, name ))

            continue


        processChunk(_CurrentChunk)

    for _CurrentChunk in doc.chunks:
        if isMarkered(_CurrentChunk) == False:
            _CurrentChunk.detectMarkers(tolerance=60)
            doc.save()
    exportObjLoop(overwrite = False)


    PhotoScan.app.messageBox("Script Complete! Hooray!!!")

def partiallyProcessAll():

    for _CurrentChunk in doc.chunks:
            #PhotoScan.app.messageBox("Starting:  " + _CurrentChunk.label) ##stops script, messagebox shows name of chunk
            print(_CurrentChunk.label)
            alignment(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            lowError(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            exportObj(_CurrentChunk)

    PhotoScan.app.messageBox("Script Complete! Hooray!!!")

def isTextured(_CurrentChunk):

    if _CurrentChunk.model.meta['atlas/atlas_blend_mode']:
        print("This chunk already has a texture:  " + _CurrentChunk.label)
        return True
    else:
        print("This chunk does not have a texture:  " + _CurrentChunk.label)
        return False

def isMarkered(_CurrentChunk):
    if len(_CurrentChunk.markers) > 0:
        print("Markers marked for:" + _CurrentChunk.label)
        return True
    else:
        print ("No markers found: " + _CurrentChunk.label)
        #_CurrentChunk.detectMarkers(tolerance=60)
        return False

def getPath():
    path = PhotoScan.app.getSaveFileName("Save Project As")  + ".psx"
    doc.save(path)
    print("Saved to path:  " + path)

def isSaved():
    if doc.path == "":
        print("Not saved")
        getPath()
        return False
    else:
        print("Already Saved:  ")
        print(doc.path)
        return True

def main():
    processAllChunks()

if __name__ == "__main__":
    main()














