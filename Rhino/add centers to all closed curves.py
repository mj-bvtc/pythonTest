import rhinoscriptsyntax as rs

highlight = rs.Command("SelClosedCrv")
closedcrv = rs.SelectedObjects()

rs.EnableRedraw(False)
for c in closedcrv:
    point = rs.CurveAreaCentroid(c)
    #print point
    rs.AddPoint(point[0])

rs.EnableRedraw(True)