import rhinoscriptsyntax as rs


texts = rs.GetObjects("Select Text objects", filter = rs.filter.annotation)

rs.EnableRedraw(False)

for t in texts:
    info = rs.TextObjectText(t)
    pt = rs.TextObjectPoint(t)
    #layer = rs.ObjectLayer(t)
    dot = rs.AddTextDot(info, pt)
    #rs.ObjectLayer(dot, layer=layer)
    color = rs.ObjectColor(t)
    rs.ObjectColor(dot, color=color)

rs.EnableRedraw(True)

