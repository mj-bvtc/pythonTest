import rhinoscriptsyntax as rs


texts = rs.GetObjects("Select Text objects", filter = rs.filter.annotation)

rs.EnableRedraw(False)

for t in texts:
    info = rs.TextObjectText(t)
    pt = rs.TextObjectPoint(t)
    dot = rs.AddTextDot(info, pt)

rs.EnableRedraw(True)

