import rhinoscriptsyntax as rs

pre = raw_input("Type Block Style Prefix")
#rs.Command("_SelBrush SelectionMode=Crossing BrushWidth=40 Polyline=No")

#points = rs.SelectedObjects()
points = rs.GetObjects()

rs.EnableRedraw(False)
for p in points:
    rs.AddTextDot(pre, p)
rs.EnableRedraw(True)
