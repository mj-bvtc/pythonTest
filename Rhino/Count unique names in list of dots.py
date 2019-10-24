import rhinoscriptsyntax as rs


objs = rs.GetObjects()

names = []
for o in objs:
    name = rs.TextDotText(o)
    names.append(name)
    


cut_names = list(set(names))

print len(cut_names)

print cut_names