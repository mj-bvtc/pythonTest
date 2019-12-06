import rhinoscriptsyntax as rs
import Rhino


guids = rs.GetObjects()

uids_dot = dict()
uids_text = dict()
names = dict()
phases = dict()
groups = set()
priorities = dict()
bids = dict()

for g in guids:
    group = rs.ObjectGroups(g)[0]
    groups.add(group)
    
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(g)
    geo = obj.Geometry
    _type = type(geo)
    
    if _type == Rhino.Geometry.TextDot:
        uids_dot[group] = g
        
        #print "Name: {}".format(name)
        bid = rs.TextDotText(g).replace(",",":")
        bids[group] = bid
        color = rs.ObjectColor(g)
        layer = rs.ObjectLayer(g)
        phases[group] = layer.split("::")[-1]
        text = rs.TextDotText(g)
        phase = layer
        phases[group] = phase
        rs.SetUserText(g, "original_color", value=color) 
        rs.SetUserText(g, "original_layer", value=layer) 
        rs.SetUserText(g, "original_text", value=text)
        rs.SetUserText(g, "bid_line", value=bid) 
        
    if _type == Rhino.Geometry.TextEntity:
        uids_text[group] = g
        name = rs.TextObjectText(g)
        names[group] = name
        color = rs.ObjectColor(g)
        layer = rs.ObjectLayer(g)
        text = rs.TextObjectText(g)
        rs.SetUserText(g, "original_color", value=color) 
        rs.SetUserText(g, "original_layer", value=layer) 
        rs.SetUserText(g, "original_text", value=text)
        priorities[group] = layer
    #print

groups = sorted(groups)
#print names

#print phases


print "uids_dot,uids_text,group,name,phase"

for g in groups:
    name = names[g]
    phase = phases[g]
    id_dot = uids_dot[g]
    id_text = uids_text[g]
    priority = priorities[g]
    bid = bids[g]
    print "{},{},{},{},{},{},{}".format(id_dot,id_text, g, name, phase, priority, bid)