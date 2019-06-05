import rhinoscriptsyntax as rs
import re

##Takes all the block objects on a setting and prepends the layer name 
## on a dot object


texts = rs.GetObjects()

rs.EnableRedraw(False)

for t in texts:
    layer = rs.ObjectLayer(t)
    msg = "SURVEY"

    point = rs.TextObjectPoint(t)
    #block = rs.TextObjectText(t)
    #msg = "{} {}".format(layer, block)
    rs.AddTextDot(msg, point)
    

rs.EnableRedraw(True)