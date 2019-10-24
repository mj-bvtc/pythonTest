import rhinoscriptsyntax as rs
import re

dots = rs.GetObjects()
areas = set()

for d in dots:
    name = rs.TextDotText(d)
    pat = r"Area\s([\d]*)"
    area = int(re.search(pat, name).group(1))
    areas.add(area)


areas = sorted(areas)

for i, a in enumerate(areas):
    print "{}. {}".format(str(i+1), a)