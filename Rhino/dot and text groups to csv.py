import rhinoscriptsyntax as rs
import Rhino


guids = rs.GetObjects()

names = dict()
phases = dict()
groups = set()

for g in guids:
    group = rs.ObjectGroups(g)[0]
    groups.add(group)
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(g)
    geo = obj.Geometry
    _type = type(geo)
    
    if _type == Rhino.Geometry.TextDot:
        name = rs.TextDotText(g)
        #print "Name: {}".format(name)
        names[group] = name
        
    if _type == Rhino.Geometry.TextEntity:
        phase = rs.TextObjectText(g).replace(",", "|")
        #print "Phase/Priority: {}".format(phase)
        phases[group] = phase
    #print

groups = sorted(groups)
#print names

#print phases


print "group, name, phase"

for g in groups:
    name = names[g]
    phase = phases[g]
    print "{},{},{}".format(g, name, phase)
