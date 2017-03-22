import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
doc = Rhino.RhinoDoc.ActiveDoc


rs.Command("_BoundingBox _pause _enter")
box = rs.LastCreatedObjects(select=True)
rs.Command("_Silhouette enter")
rs.DeleteObject(box)edi

