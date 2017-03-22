import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

###select block
block = rs.GetObject("Select Polysrf")

###get bounding box
box = rs.BoundingBox(block)
bbox = rg.BoundingBox(box)
minPt = bbox.Corner(True, True, True)
maxPt = bbox.Corner(False, False, False)


if minPt:
    print "min Pt is: " + minPt.ToString()
if maxPt:
    print "max Pt is: " + maxPt.ToString()

###record dimensions of block
dx = abs(minPt[0]-maxPt[0])
dy = abs(minPt[1]-maxPt[1])
dz = abs(minPt[2]-maxPt[2])

width, length, height = dx, dy, dz

print width
print length
print height



###get section
sectionLine = rs.GetLine()
section = rs.AddCurve(sectionLine)
profile = rs.ProjectCurveToSurface(section, block, rg.Vector3d(0,0,1))


###get plane that section lies on
centroidTuple = rs.CurveAreaCentroid(profile)
centroid = centroidTuple[0]
rs.AddPoint(centroid)

    ###get 3 non co linear points from section
    
curves = rs.ExplodeCurves(section)


print curves



#rs.PlaneFromFrame()

#rg.Plane(centroid, normal)


###move section to top view/projected to XY plane


###move to origin

###get bounding box

###get width X and height Y, dimension them

###label block

###simplify curves

###rebuild curves to .005" tolerance

###offset out 1/32" (compensate for wire width)

###delete other line

###connect lead in and lead out line

###convert to gcode, with wirecode instructions start/end

###write gcode to .txt file in proper directory



#profileCentroid = rg.AreaMassProperties.Compute(profile)
#centroid = profileCentroid.Centroid()
#profilePlane = 
#xy = rg.Plane.WorldXY
##Rhino.Geometry.Transform xform = Rhino.Geometry.Transform.PlaneToPlane(source_plane, target_plane)