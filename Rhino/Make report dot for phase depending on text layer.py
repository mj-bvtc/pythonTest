import rhinoscriptsyntax as rs
import re

##Takes all the block objects on a setting and prepends the layer name 
## on a dot object


texts = rs.GetObjects()

rs.EnableRedraw(False)

for t in texts:
    layer = rs.ObjectLayer(t)
    msg = None
    if "BASE" in layer.upper():
        #print "Base"
        msg = "BASE"
    if "CHANGE ORDER" in layer.upper():
        #print "CO"
        pat = r"CO[\s\d]*"
        result = re.findall(pat, layer)
        if result:
            #print result[0]
            msg = result[0]
    point = rs.TextObjectPoint(t)
    #block = rs.TextObjectText(t)
    #msg = "{} {}".format(layer, block)
    rs.AddTextDot(msg, point)
    

rs.EnableRedraw(True)