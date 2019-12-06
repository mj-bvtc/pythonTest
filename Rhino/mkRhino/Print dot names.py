import rhinoscriptsyntax as rs


dots = rs.GetObjects()

for d in dots:
    name = rs.TextDotText(d)
    priority = rs.GetUserText(d, key="priority")
    print d, name, priority
    #if priority != "P6":
        #print "{},{}".format(name, priority)