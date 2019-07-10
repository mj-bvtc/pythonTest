import rhinoscriptsyntax as rs
import Rhino

objs = rs.GetObjects()

factor = 50

box = rs.BoundingBox(objs)
box = Rhino.Geometry.BoundingBox(box)
box.Inflate(factor,factor,factor)
box = box.GetCorners()
#Rhino.Geometry.BoundingBox.Inflate(10,10,10)

#Rhino.Geometry.BoundingBox.GetCorners()


rs.ZoomBoundingBox(box)