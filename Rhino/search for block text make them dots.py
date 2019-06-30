import rhinoscriptsyntax as rs


objs = rs.GetObjects()


for o in objs:
    name = rs.TextObjectText(o)
    point = rs.TextObjectPoint(o)
    if name == "B17A":
        rs.AddTextDot(name, point)