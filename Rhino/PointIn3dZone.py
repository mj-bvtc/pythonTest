import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino

class Zone:
    
    def __init__(self):
        self.type = None
        self.value = None
        self.brep = None
        self.point_inside = None
        self.id = None
    
    def get_brep(self):
        self.id = rs.GetObject("get brep", rs.filter.extrusion)
        self.brep = rs.coercebrep(self.id)
    
    def set_id(self, guid):
        self.id = guid
        self.brep = rs.coercebrep(self.id)

    def check_point_inside(self, point):
        self.point_inside = self.brep.IsPointInside(point, rs.UnitAbsoluteTolerance(), False)
        return self.point_inside

    def report(self):
        if self.point_inside is True:
            message = "Point is on {} '{}'".format(self.type, self.value)
        else:
            message = "Point is outside of {} '{}'".format(self.type, self.value)
        print message


def main():
    """
    point = rs.coerce3dpoint(rs.GetObject("get point", rs.filter.point))
    zz = Zone()
    zz.get_brep()
    zz.value = 12
    zz.type = "Drop"
    z = Zone()
    z.value = 22
    z.type = "Floor"
    z.get_brep()
    z.check_point_inside(point)
    zz.check_point_inside(point)
    z.report()
    zz.report()
    """
    a = Zone()
    a.set_id("441e600b-481b-4381-931e-5fc36a44e11e")
    a.type = "Floor"
    a.value = "Ground"
    
    b = Zone()
    b.set_id("d71f3912-29b9-489a-b9ec-2547719bbd9f")
    b.type = "Side"
    b.value = "East"
    
    c = Zone()
    c.set_id("77ba7ebf-168d-4c24-81ed-a84a41fc7f47")
    c.type = "Feature"
    c.value = "Upper Dome"
    
    
    point = Rhino.Geometry.Point3d(1152.27,2113.63,994.474)
    for zone in [a, b, c]:
        zone.check_point_inside(point)
        zone.report()


if __name__ == "__main__":
    main()
