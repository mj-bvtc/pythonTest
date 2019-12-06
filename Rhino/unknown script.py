import rhinoscriptsyntax as rs
import Rhino

spheres = rs.GetObjects()

for s in spheres:
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(s)
    #Rhino.Geometry.Sphere.Center
    center = obj.Center()
    print center