import rhinoscriptsyntax as rs


dots = rs.GetObjects("get dots", filter = rs.filter.textdot)

for i, d in enumerate(dots):
    i += 1
    count = i
    guid = d
    name = rs.TextDotText(d)
    point = rs.TextDotPoint(d)
    layer = rs.ObjectLayer(d)
    x, y, z = point
    print "{},{},{},{},{},{},{}".format(guid, count, name, layer, x, y, z)