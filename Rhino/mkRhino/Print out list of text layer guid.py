import rhinoscriptsyntax as rs


#dots = rs.GetObjects()
#dots = [str(d) for d in dots]
#print str(dots)

dots = rs.GetObjects()
print"text,layer,guid,profile"
for d in dots:
    text = rs.TextDotText(d)
    text = text.replace(",", " + ")
    profile = rs.ObjectName(d)
    layer = rs.ObjectLayer(d) 
    guid = d
    msg = "{},{},{},{}".format(text, layer, guid, profile)
    print msg