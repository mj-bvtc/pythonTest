import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

doc = Rhino.RhinoDoc.ActiveDoc

objs = rs.GetObjects()

points = [rs.SurfaceAreaCentroid(obj)[0]  for obj in objs]
normals = []

for i, obj in enumerate(objs):
        point = points[i]
        param = rs.SurfaceClosestPoint(obj, point)
        normal = rs.SurfaceNormal(obj, param)
        normals.append(normal)




for i, point in enumerate(points):
    
    pt = rs.coerce3dpoint(point)
    vec = normals[i]
    line = rg.Line(pt, vec, 400)
    doc.Objects.AddLine(line)


rs.Redraw()