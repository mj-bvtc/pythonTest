import rhinoscriptsyntax as rs

rs.EnableRedraw(False)
dots = rs.GetObjects("get dots", filter=rs.filter.textdot)
for d in dots:
    pt = rs.TextDotPoint(d)
    rs.AddPoint(pt)

rs.EnableRedraw(True)

