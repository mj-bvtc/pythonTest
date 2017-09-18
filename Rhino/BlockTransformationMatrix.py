import Rhino
import rhinoscriptsyntax as rs

#t = rs.BlockDescription("A10")
#print t

guid = rs.GetObject()

#Rhino.Geometry.InstanceReferenceGeom
#
xform = rs.BlockInstanceXform(guid)

#print type(xform)

#Rhino.Geometry.Transform.M00

print xform
