import rhinoscriptsyntax as rs

dots = rs.GetObjects()

rs.EnableRedraw(False)
for d in dots:
    rs.TextDotText(d, text="Add")
rs.EnableRedraw(True)