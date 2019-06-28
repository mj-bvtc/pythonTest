import rhinoscriptsyntax as rs


objs = rs.GetObjects()
rs.EnableRedraw(False)
for o in objs:
    name = rs.TextDotText(o)
    if name == "X":
        rs.TextDotText(o, text="Z")

rs.EnableRedraw(True)