import uuid
import datetime
import rhinoscriptsyntax as rs
import Rhino
import getpass
import socket

#adding incremental text dots at different points
def count(num):
    for i in range(num):
        pt = rs.GetPoint("Select point")
        rs.AddTextDot("hello {} {}".format(i, pt), pt)
        


#encapsulation
"""Value
 Description
 
0
 The point is outside of the closed curve.
 
1
 The point is inside of the closed curve.
 
2
 The point is on the closed curve.
 
"""

#point in circle (always inside; result will be 1)

def point_in_circle():
    point = rs.GetPoint("Pick Point")
    curve = rs.AddCircle(point, 5)
    
    result = rs.PointInPlanarClosedCurve(point, curve)
    print result
    return result

def point_in_cls_crv():
    n6 = rs.GetObject("Select closed curve")
    point = rs.GetPoint("Select where to add test point")
    p = rs.coerce3dpoint(rs.AddPoint(point))
    
    result = rs.PointInPlanarClosedCurve(p, n6)
    print result
    return result

class Common(object):
    def __init__(self):
        self.guid = uuid.uuid4()
        self.created_datetime = datetime.datetime.now()
        self.user_name = getpass.getuser()
        self.user_computer = socket.gethostname()


class Zone(Common):
    def __init__(self):
        super(Zone, self).__init__()
        self.name = None
        self.curve = None
        self.type = None   # ex. 'floor', 'drop', 'region', 'elevation', 'area'
    

class Block(Common):
    def __init__(self):
        super(Block, self).__init__()
        self.name = None
        self.point = None


def point_in_cls_crv(point, zone):
    curve = zone.curve
    result = rs.PointInPlanarClosedCurve(point, curve)
    if result == 1:
        print "point in zone: {}".format(zone.name)
    else:
        print "point not in zone: {}".format(zone.name)
    return result


def main():
    zones = []
    inside = []
    
    point = rs.GetObject("Pick Test Point", filter=1)
    
    for i in range(2):
        z = Zone()
        curve = rs.GetObject("Select Zone (Closed Curve)", filter=4)
        name = raw_input("Name for Zone: ")
        z.name = name
        z.curve = curve
        zones.append(z)    
        result = point_in_cls_crv(point, z)
        if result == 1:
            inside.append(z)
    print inside

if __name__ == "__main__":
    main()
    



