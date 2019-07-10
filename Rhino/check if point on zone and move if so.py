import rhinoscriptsyntax as rs
import Rhino

dots = rs.GetObjects("get dots")
zones = rs.GetObjects("get zones")
rs.EnableRedraw(False)
for z in zones:
    for d in dots:
        point = rs.TextDotPoint(d)
        curve = z
        result = rs.PointInPlanarClosedCurve(point, curve)
        if result == 2:
            print d
            translation = Rhino.Geometry.Vector3d(.01,.01,0)
            rs.MoveObject(d, translation)
            print "object moved"
            print
            
rs.EnableRedraw(True)