import rhinoscriptsyntax as rs


obs = rs.GetObjects()

rs.EnableRedraw(False)

for o in obs:
    
    layer = rs.ObjectLayer(o)
    rs.TextDotText(o, text=layer)

rs.EnableRedraw(True)
