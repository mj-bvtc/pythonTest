import rhinoscriptsyntax as rs


rs.Command("_SelDot")
dots = rs.SelectedObjects()


rs.EnableRedraw(False)
for d in dots:
    point = rs.TextDotPoint(d)
    rs.AddPoint(point)
    rs.HideObject(d)
rs.EnableRedraw(True)