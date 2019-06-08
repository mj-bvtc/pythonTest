import rhinoscriptsyntax as rs
import Rhino

dots = rs.GetObjects("Select dots", rs.filter.textdot)
zones = rs.GetObjects("Select zones", rs.filter.curve)

for d in dots:
    point = rs.TextDotPoint(d)
    name = rs.TextDotText(d)
    for z in zones:
        test = rs.PointInPlanarClosedCurve(point, z)
        if test == 2:
            rs.ObjectName(z, name=name)



