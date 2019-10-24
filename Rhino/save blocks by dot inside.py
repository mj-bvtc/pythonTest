import rhinoscriptsyntax as rs

dots = rs.GetObjects("get dots")
curves = rs.GetObjects("get curves")


rs.EnableRedraw(False)

for d in dots:
    name = rs.TextDotText(d)
    point = rs.TextDotPoint(d)
    for c in curves:
        test = rs.PointInPlanarClosedCurve(point, c)
        if test == 1:
            rs.ObjectName(c, name=name)

rs.EnableRedraw(True)