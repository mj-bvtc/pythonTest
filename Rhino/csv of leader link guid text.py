import rhinoscriptsyntax as rs
import Rhino

leaders = rs.GetObjects()

for i in leaders:
    guid = i
    text = rs.LeaderText(i)
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(i)
    link = obj.Attributes.Url
    layer = rs.ObjectLayer(i)
    
    #print i, text, obj, link
    line = "{},{},{},{},{}".format(i, text, obj, link,layer)
    print line