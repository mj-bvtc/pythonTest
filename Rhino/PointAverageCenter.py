import rhinoscriptsyntax as rs




points = rs.GetObjects()


xs = 0
ys = 0
zs = 0
for point in points:
    x, y, z  = rs.PointCoordinates(point)
    
    xs += x
    ys += y
    zs += z

x_average = xs/len(points)
y_average = ys/len(points)
z_average = zs/len(points)

ave = rs.AddPoint(x_average, y_average, z_average)



