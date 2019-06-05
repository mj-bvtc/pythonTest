import rhinoscriptsyntax as rs


dots = rs.GetObjects("Get dots")

rs.EnableRedraw(False)

for d in dots:
    name = rs.TextDotText(d)
    if name != "X":
        rs.ObjectLayer(d, layer="named")

rs.EnableRedraw(True)