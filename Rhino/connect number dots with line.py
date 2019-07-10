import rhinoscriptsyntax as rs
import operator

objs = rs.GetObjects()

blocks = {}

for o in objs:
    num = int(rs.TextDotText(o))
    guid = o
    blocks[guid] = num 

sorted_list = sorted(blocks.items(), key=operator.itemgetter(1))


points = []

rs.EnableRedraw(False)
for item in sorted_list:
    point = rs.TextDotPoint(item[0])

    #print point
    points.append(point)

for i, p in enumerate(points):
    if i == len(points)-1:
        pass
    else:
        rs.AddLeader([points[i+1], p], view_or_plane="Front", text="")   # MAKE SURE YOU ARE IN THE CORRECT VIEW, THIS WILL FAIL OTHERWISE
        #line = rs.AddLine(p, points[i+1])
rs.EnableRedraw(True)