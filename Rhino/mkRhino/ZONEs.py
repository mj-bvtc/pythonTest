import rhinoscriptsyntax as rs
import Rhino


class Zone:
    Gcount = 1
    Gzones = []

    def __init__(self, name=None, curve=None):
        self.count = Zone.Gcount
        Zone.Gcount += 1
        self.curve = curve
        self.name = name


    def get_curve(self):
        crv = rs.GetObject("Select Closed Curve", rs.filter.curve)
        if rs.IsCurveClosed(crv) is True:
            self.curve = crv
            #self.get_name()
        else:
            print "This curve is not closed"
    def get_name(self):
        name = rs.GetString("Type in zone name")
        if name is not None:
            self.name = name
            print "Named zone: {}".format(self.name)
    
    def auto_name(self):
        alpha = "abcdefghijklmnopqrstuvwxyz"
        letters = list(alpha)
        self.r3name = letters[self.Gcount]
    
    @classmethod
    def from_crv_list(cls, list, index):
        zone = cls()
        
        

def find_point(point, zones):
    for zone in zones:
        result = rs.PointInPlanarClosedCurve(point, zone.curve)
        if result == 1:
            print "Point in zone '{}'".format(zone.name)
        else:
            print "Point not in zone '{}'".format(zone.name)

def point_in_zone(point, zone):
    result = True if rs.PointInPlanarClosedCurve(point, zone.curve) == 1 else False
    return result


def point_zones(point, zones):
    matches = [x.name for x in zones if point_in_zone(point, x) is True]
    print "Point in {}".format(matches)

def main():
    pt = rs.GetObject("Select point 1", rs.filter.point)
    zlist = []
    for i in range(10):
        x = Zone()
        zlist.append(x)
    point_zones(pt, zlist)


if __name__ == "__main__":
    main()