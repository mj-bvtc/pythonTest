import rhinoscriptsyntax as rs


dots = rs.GetObjects()

print "guid,group,name,layer,category"

for d in dots:
    guid = d
    group = "NA"
    name = rs.TextDotText(d)
    phase = "Mickey Adds"
    status = rs.GetUserText(d, key="original_layer")
    msg = "{},{},{},{},{}".format(guid,group,name,phase,status)
    print msg

