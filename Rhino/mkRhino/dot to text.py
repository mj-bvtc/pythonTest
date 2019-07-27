import rhinoscriptsyntax as rs


dots = rs.GetObjects("Select dot objects", filter = rs.filter.textdot)

rs.EnableRedraw(False)

for d in dots:
    info = rs.TextDotText(d)
    pt = rs.TextDotPoint(d)
    layer = rs.ObjectLayer(d)
    dot = rs.AddText(info, pt, height=.08, justification=131074)
    rs.ObjectLayer(dot, layer)
    

rs.EnableRedraw(True)

