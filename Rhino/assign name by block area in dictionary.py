import rhinoscriptsyntax as rs


curves = rs.GetObjects()

names = dict()

rs.EnableRedraw(False)

for c in curves:
    name = rs.ObjectName(c)
    area = round(rs.CurveArea(c)[0], -1)
    centroid = rs.CurveAreaCentroid(c)
    if name in names:
        names[name].append(area)
    else:
        names[name] = [area]


for key in names:
    key
    value = sorted(list(set(names[key])))
    names[key] = value

unique = set()

for c in curves:
    name = rs.ObjectName(c)
    area = round(rs.CurveArea(c)[0], -1)
    centroid = rs.CurveAreaCentroid(c)[0]
    instance = names[name].index(area) + 1
    new_name = name + str(instance)
    dot = rs.AddTextDot(new_name, centroid)
    unique.add(new_name)

rs.EnableRedraw(True)

print len(unique)