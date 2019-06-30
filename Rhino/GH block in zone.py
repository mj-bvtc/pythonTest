import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino







class block:
    
    def __init__(self):
        self.point = None
        self.layer = None
        self.name = None
        self.drop = None
        self.floor = None
        self.guid = None
        self.zones = []


class zone:
    
    def __init__(self):
        self.name = None
        self.guid = None
        self.curve = None




def point_in_zone(point, zone):
    result = True if rs.PointInPlanarClosedCurve(point, zone.curve) == 1 else False
    return result

def point_zones(point, zones):
    matches = [x.name for x in zones if point_in_zone(point, x) is True]
    #print "Point in {}".format(matches)
    return matches

def load_zones(file):
    
    with open(file, "r") as f:
        content = f.readlines()
        content = [x.strip() for x in content] 
        return content


blocks = []

for i,id in enumerate(block_guid):
    b = block()
    b.guid = id
    b.name = block_name[i]
    b.point = block_pt[i]
    b.layer = block_layer[i]
    blocks.append(b)

zones = []

for i, id in enumerate(zone_guid):
    z = zone()
    z.name = zone_name[i] 
    z.guid = id
    z.curve = zone_crv[i]
    zones.append(z)

#sc.doc = Rhino.RhinoDoc.ActiveDoc

for b in blocks:
    for z in zones:
        test = rs.PointInPlanarClosedCurve(b.point, z.curve)
        if test > 0:
            #print test
            b.zones.append(z.name)
            print "{} in {}".format(b.name, z.name)
        #print b.point

#sc.doc = ghdoc







