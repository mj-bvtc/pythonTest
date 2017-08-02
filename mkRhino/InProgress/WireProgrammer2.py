import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
doc = Rhino.RhinoDoc.ActiveDoc


#section object
cmd = "-_Section JoinCurves=ByPolysurface "
rs.Command(cmd, False)

#put object at origin on xy plane
section = rs.LastCreatedObjects(select=True)
cmd = "SetMaximizedViewport perspective "
cmd = "-_CPlane _Object"
rs.Command(cmd, False)
cmd = "-_RemapCPlane _View top"
rs.Command(cmd, False)
section = rs.LastCreatedObjects(select=True)
cmd = "_Invert _Hide"
rs.Command(cmd, False)

#maximize top view
cmd = "SetMaximizedViewport top "
rs.Command(cmd, False)
rs.ZoomExtents()

#rotate so bottom is flat
origin = [0,0,0]
rotate = int(raw_input("Type in rotation angle (degrees)"))
directionPositive = raw_input("clockwise or counterclockwise?")
if directionPositive.upper() == "CLOCKWISE".upper():
    rotate *= -1
rs.RotateObject(section, origin, rotate)


#offset section
offset = 1/32
direction = [1000, 1000, 0]
section2 = rs.OffsetCurve(section, direction, offset)
rs.DeleteObject(section)
section = section2

#move to origin again
rs.SelectObject(section)
cmd = "_BoundingBox enter enter"
rs.Command(cmd, False)
box = rs.LastCreatedObjects(select=False)

points = rs.CurvePoints(box)
start_point = points[0]
dx = start_point[0] * -1
dy = start_point[1] * -1
translation = [dx, dy, 0]
rs.MoveObject(section, translation)
rs.MoveObject(box, translation)

#offset box
direction = [1000, 1000, 0]
distance = .2
box2 = rs.OffsetCurve(box, direction, distance)
rs.DeleteObject(box)

#lead in out
#rs.SplitCurve()


