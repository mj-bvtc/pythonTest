import rhinoscriptsyntax as rs


objects = rs.GetObjects(message="Select text dots", filter=rs.filter.textdot)


print "guid, layer, count"

for ob in objects:
    layer = rs.ObjectLayer(ob, layer=None)
    count = rs.TextDotText(ob, text=None)
    msg = "{},{},{}".format(ob, layer, count)
    
    print msg