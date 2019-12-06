import rhinoscriptsyntax as rs
import Rhino

hatches = rs.GetObjects()
rs.EnableRedraw(False)
for h in hatches:
    
    layer = rs.ObjectLayer(h)
    last_layer = layer.split("::")[-2:]
    #Rhino.Geometry.Hatch.BasePoint
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(h)
    pt = obj.Geometry.BasePoint
    
    #print last_layer
    #print pt
    
    #rs.AddText(last_layer, pt, height=10)
    
    box = obj.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY)
    #Rhino.Geometry.BoundingBox.Center
    #Rhino.Geometry.Hatch.GetBoundingBox(
    #Rhino.Geometry.Plane.WorldXY
    center = box.Center
    
    
    rs.AddText(last_layer, center, height=1)
rs.EnableRedraw(True)