import rhinoscriptsyntax as rs
import operator
import re

def sort_human(l):
    l = [str(x) for x in l]
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [ convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]+)', key) ]
    l.sort( key=alphanum )
    return l

objs = rs.GetObjects()

ordered_names = sort_human([rs.TextDotText(x) for x in objs])

class area:
    def __init__(self):
        self.guid = None
        self.name = None
        self.point = None
        self.order = None

classes = []

for o in objs:
    a = area()
    a.guid = o
    a.name = rs.TextDotText(o)
    a.point = rs.TextDotPoint(o)
    a.order = ordered_names.index(a.name)
    classes.append(a)

classes.sort(key=operator.attrgetter('order'))


points = [x.point for x in classes]

rs.EnableRedraw(False)


for i, p in enumerate(points):
    if i == len(points)-1:
        pass
    else:
        rs.AddLeader([points[i+1], p], view_or_plane="Top", text="")   # MAKE SURE YOU ARE IN THE CORRECT VIEW, THIS WILL FAIL OTHERWISE
        #line = rs.AddLine(p, points[i+1])
rs.EnableRedraw(True)