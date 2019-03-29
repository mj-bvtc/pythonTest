import rhinoscriptsyntax as rs


text = rs.GetObjects("get txt")


rs.EnableRedraw(False)
for t in text:
    pt = rs.TextObjectPoint(t)
    point = rs.AddPoint(pt)
    color = rs.ObjectColor(t)
    rs.ObjectColor(point, color)
rs.EnableRedraw(True)