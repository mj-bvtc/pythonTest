import rhinoscriptsyntax as rs




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


def convert_zone(file):
    text = load_zones(file)
    zones = []
    for i in text:
        j = i.split(",")
        z = zone()
        z.name = j[0]
        z.guid = j[1]
        z.curve = j[2]
        zones.append(z)
    return zones





def main():
    
    
    
    block_instances = rs.GetObjects("Select Blocks")
    
    rs.EnableRedraw(False)
    
    zones = convert_zone(r"C:\Users\mkreidler\Desktop\zones copy.txt")
    blocks = []
    for t in block_instances:
        b = block()
        b.point = rs.BlockInstanceInsertPoint(t)
        b.layer = rs.ObjectLayer(t)
        b.name = str(rs.BlockInstanceName(t)).replace(",", " + ")
        b.guid = t
    
        b.zones = str(point_zones(b.point, zones)).replace(",", "//")
    
    
        blocks.append(b)
        #print b.zones
    rs.EnableRedraw(True)
    path = r"C:\Users\mkreidler\Desktop\171_Zone_output.txt"
    try:
        
        
        f = open(path, 'w+')
        f.write("layer,name,zones,guid\n")
        for b in blocks:
            message = "{},{},{},{},{}\n".format(b.layer, b.name, b.zones, b.guid,b.point)
            f.write(message)
        
        
        
    finally:
        print "saved file: {}".format(path)
        f.close()
    
    

if __name__ == "__main__":
    main()