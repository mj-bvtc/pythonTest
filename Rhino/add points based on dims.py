import rhinoscriptsyntax as rs

dims = rs.GetObjects()

lens = []

for d in dims:
    
    l =  rs.DimensionValue(d)
    lens.append(l)

start = rs.GetPoint()

rs.EnableRedraw(False)
for l in lens:
    x,y,z = start
    newpt = x+l, y, z
    rs.AddPoint(newpt)
rs.EnableRedraw(True)

