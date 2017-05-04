import rhinoscriptsyntax as rs

obj = rs.GetObject("Click object")
box = rs.BoundingBox(obj)
ptList = []
for i, point in enumerate(box):
    pt = point
    p = rs.coerce3dpoint(pt)
    ptList.append(p)
    

newList = []
for item in ptList:
    x,y,z = item
    pt = (x,y,z)
    newList.append(pt)

set = set(newList)
points = []

for item in set:
    pt = rs.AddPoint(item)
    points.append(pt)
lines = []
count = 0 

for i in range(len(points)):
    
    if count == len(points)-1:
        
        line = rs.AddLine(points[count],points[0])        
        lines.append(line)
        break                 
    line = rs.AddLine(points[count], points[count+1])
    lines.append(line)
    count +=1
    


rs.SelectObject(points[0])
