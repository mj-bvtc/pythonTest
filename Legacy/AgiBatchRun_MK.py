import PhotoScan
import os
import math
import itertools

doc = PhotoScan.app.document
messageList = []


def alignment(_CurrentChunk):
    #initial alignment 
    _CurrentChunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection)
    _CurrentChunk.alignCameras()
    initialPointCount = len(_CurrentChunk.point_cloud.points)
    messageList.append("Original Point initialPointCount: ")
    messageList.append(initialPointCount)

def error(_CurrentChunk):

    # Compatibility - Agisoft PhotoScan Professional 1.2.4
    # saves reprojection error for the tie points in the sparse cloud 


    import PhotoScan
    import math
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
    messageList.append("initial points: " + str(initialPtCount))


    #initial settings before loop\
    
    error1 = error(_CurrentChunk)

    initialPts = initialPtCount
    currentPts = initialPts
    count = 0
    while error1 >= 1.000:
        #prints current error as it goes through loop
        messageList.append("initial error: " + str(error1))

        #breaks if half points or more removed
        if initialPts*.50 > currentPts:
            messageList.append("Percentage of points removed too high, I stopped it")
            break

        tiePtCount = len(_CurrentChunk.point_cloud.points)
        #breaks if less than 40K points are left
        if tiePtCount < 5000:
            messageList.append("Point count almost went below 40,000, I stopped it")
            break

        #breaks if loop runs more than 1K times
        if count > 100:
            messageList.append("This may have ran forever, I stopped it")
            break

        #optimize camera alignment before removing points
        _CurrentChunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_b1=True, fit_b2=True, fit_k1k2k3=True,fit_p1p2=True, fit_k4=True, fit_p3=True, fit_p4=True)

        #remove error by %, lower point count (for simulation only), advance count by 1
        error1 *= .80
        #currentPts -= 500
        count += 1
        _CurrentChunk.buildPoints(error = (_CurrentChunk.buildPoints(error1)))

    #prints total number of times loop ran
    messageList.append("While loop ran " + str(count) + " times")
    messageList.append("Number of points after gradual selection: ")
    messageList.append(len(_CurrentChunk.point_cloud.points))

def processChunk(_CurrentChunk):

    #Process Chunks after the initial alignment and gradual selection 
    _CurrentChunk.buildDenseCloud(quality=PhotoScan.HighQuality)
    doc.save()
    _CurrentChunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation, face_count = 2000000)
    doc.save()
    _CurrentChunk.buildUV(mapping=PhotoScan.GenericMapping)
    doc.save()
    _CurrentChunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
    doc.save()
    _CurrentChunk.detectMarkers()
    doc.save()

def exportObj(_CurrentChunk):
   
    docName = doc.path.split("/")[-1]
    folder = doc.path.rstrip(docName)
    
   
    # exports obj
    name = _CurrentChunk.label
    subFolder = folder + name + "/"
    printList = []
    if os.path.exists(subFolder):
        file = subFolder + name + ".obj"
        _CurrentChunk.exportModel(file)
        messageList.append("attempted to export: " + file)
    else:
        messageList.append(subFolder + " did not exist, made folder anyways")
        os.makedirs(subFolder)
        file = subFolder + name + ".obj"
        _CurrentChunk.exportModel(file)
        messageList.append("attempted to export: " + file)

    doc.save()

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
    #messageList.append(combos)

    camList = []
    for cam in _CurrentChunk.cameras:
        if cam.center != None:

            pointList.append(cam.center)
            camList.append(cam.label)

    #print(pointList)

    ptCombos = list(itertools.combinations(pointList,2))

    #messageList.append(ptCombos)


    distList = []

    a = [0,0,0]
    b = [8,0,0]

    testDist = ptdist(a,b)
    #messageList.append(testDist)



    for pt in ptCombos:
        
        dist = ptdist(pt[0],pt[1])
        distList.append(dist)
        


    

    maxDist = max(distList) #biggest distance
    messageList.append(maxDist)

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

    messageList.append("After cropping points too far from cameras there were: ")
    messageList.append(camCropPtList)

    message = cam1 + " and " + cam2 + " are the farthest photos apart from each other.  They are " + str(maxDist) + " units apart from one another."
    message += " They are located at " + str(f1) + " and " + str(f2)
    message += " Halfway between them is " + str(center) + " A selection of nearby points will be made, and those points will be cropped. Thanks, and have a greeeeat day"
    messageList.append(message)

def processAllChunks():

    for _CurrentChunk in doc.chunks:
            #PhotoScan.app.messageBox("Starting:  " + _CurrentChunk.label) ##stops script, messagebox shows name of chunk
            messageList.append(_CurrentChunk.label)
            alignment(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            lowError(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            processChunk(_CurrentChunk)
            exportObj(_CurrentChunk)

    print(messageList)
    PhotoScan.app.messageBox("Script Complete! Hooray!!!")

def partiallyProcessAll():

    for _CurrentChunk in doc.chunks:
            #PhotoScan.app.messageBox("Starting:  " + _CurrentChunk.label) ##stops script, messagebox shows name of chunk
            messageList.append(_CurrentChunk.label)
            alignment(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
            lowError(_CurrentChunk)
            cropPtFromCameras(_CurrentChunk)
    print(messageList)
    PhotoScan.app.messageBox("Script Complete! Hooray!!!")


processAllChunks()











