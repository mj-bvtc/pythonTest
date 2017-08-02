import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
doc = Rhino.RhinoDoc.ActiveDoc


###insert clipboard object at point
cmd = "'_Paste"
rs.Command(cmd, False)
objs = rs.LastCreatedObjects(select=True)
destination = rs.GetPoint("Choose a point to place object")

#calculate initial point and placement point
pt = rs.CurveStartPoint(objs[0])
dx = destination[0] - pt[0]
dy = destination[1] - pt[1]
dz = destination[2] - pt[2]
translation = [dx, dy, dz]
rs.MoveObjects(objs, translation)


