import rhinoscriptsyntax as rs




circles = rs.GetObjects()

for ci in circles:
    center = rs.CircleCenterPoint(ci)
    print center
    rs.AddPoint(center)