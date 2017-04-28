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

    def check_point_inside(self, point):
        self.point_inside = self.brep.IsPointInside(point, rs.UnitAbsoluteTolerance(), False)
        return self.point_inside

    def report(self):
        if self.point_inside is True:
            message = "Point is on {} {}".format(self.type, self.value)
        else:
            message = "Point is outside of {} {}".format(self.type, self.value)
        print message

def main():
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



if __name__ == "__main__":
    main()
