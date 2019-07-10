import rhinoscriptsyntax as rs


rs.Command("_SelDot")
dots = rs.SelectedObjects()


rs.EnableRedraw(False)
for d in dots:
    point = rs.TextDotPoint(d)
    name = rs.TextDotText(d)
    pt = rs.AddPoint(point)
    rs.HideObject(d)
    rs.ObjectName(pt, name = name)
rs.EnableRedraw(True)