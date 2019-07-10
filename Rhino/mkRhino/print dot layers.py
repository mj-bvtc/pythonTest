import rhinoscriptsyntax as rs

objs = rs.GetObjects()
rs.EnableRedraw(False)
for o in objs:
    layer = rs.ObjectLayer(o)
    print layer
    
rs.EnableRedraw(False)