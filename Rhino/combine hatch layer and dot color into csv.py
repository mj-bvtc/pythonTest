import rhinoscriptsyntax as rs
import Rhino


guids = rs.GetObjects()

uids = dict()
names = dict()
phases = dict()
groups = set()
cats = dict()

for g in guids:
    group = rs.ObjectGroups(g)[0]
    groups.add(group)
    
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(g)
    geo = obj.Geometry
    _type = type(geo)
    
    if _type == Rhino.Geometry.TextDot:
        uids[group] = g
        name = rs.TextDotText(g)
        #print "Name: {}".format(name)
        names[group] = name
        color = rs.ObjectColor(g)
        layer = rs.ObjectLayer(g)
        cats[group] = layer.split("::")[-1]
        text = rs.TextDotText(g)
        rs.SetUserText(g, "original_color", value=color) 
        rs.SetUserText(g, "original_layer", value=layer) 
        rs.SetUserText(g, "original_text", value=text) 
        
    if _type == Rhino.Geometry.Hatch:
        color = rs.ObjectColor(g)
        layer = rs.ObjectLayer(g)
        rs.SetUserText(g, "original_color", value=color) 
        rs.SetUserText(g, "original_layer", value=layer) 
        phases[group] = layer
    #print

groups = sorted(groups)
#print names

#print phases


print "guid, group, name, phase"

for g in groups:
    name = names[g]
    phase = phases[g]
    uid = uids[g]
    cat = cats[g]
    print "{},{},{},{},{}".format(uid, g, name, phase, cat)