import rhinoscriptsyntax as rs


srfs = rs.GetObjects()

rs.EnableRedraw(False)
for s in srfs:
    center = rs.SurfaceAreaCentroid(s)[0]
    #rs.SurfaceAreaCentroid(
    note = "G"
    rs.AddTextDot(note, center)
rs.EnableRedraw(True)