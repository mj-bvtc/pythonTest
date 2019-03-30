import rhinoscriptsyntax as rs

file = rs.OpenFileName()

if not file:
    print "Failed"


f = open(file, "r")

rs.EnableRedraw(False)

for line in f:
    #print line
    rs.SelectObject(line)


rs.EnableRedraw(True)