import rhinoscriptsyntax as rs

zones = rs.GetObjects()

for zone in zones:
    
    name = rs.ObjectName(zone)
    #print name
    if name == "":
        print "bad"
        pass
    else:
        print "good"
        pass
print "done"