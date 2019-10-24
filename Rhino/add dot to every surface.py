import rhinoscriptsyntax as rs

srfs = rs.GetObjects()


rs.EnableRedraw(False)

for s in srfs:
    point = rs.SurfaceAreaCentroid(s)[0]
    rs.AddTextDot("Add", point)


rs.EnableRedraw(True)