import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg

doc = Rhino.RhinoDoc.ActiveDoc

dot_guids = rs.GetObjects()

for id in dot_guids:
    geo = doc.Objects.Find(id)
    print geo.Geometry.Point
    print geo.Geometry.Text
    print
    



