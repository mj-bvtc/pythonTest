import rhinoscriptsyntax as rs


class zone:
    
    def __init__(self):
        self.name = None
        self.guid = None
        self.curve = None


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






print convert_zone(r"C:\Users\mkreidler\Desktop\zones - Copy.txt")[0].__dict__