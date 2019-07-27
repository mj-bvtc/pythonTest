import rhinoscriptsyntax as rs


points = rs.GetObjects()

rs.EnableRedraw(False)
for p in points:
    name = rs.ObjectName(p)
    rs.AddTextDot(name, p)
rs.EnableRedraw(True)
