import math as m


class GeometryBase(object):
    """This is the base class uniting all geometries"""
    def __init__(self):
        self.id = None
        self.is2D = None
        self.is3D = None


def pythagorean_theorem(a, b):
    c = m.sqrt(a**2 + b**2)
    return c


def point_distance(a, b):
    x1, y1, z1 = a.x, a.y, a.z
    x2, y2, z2 = b.x, b.y, b.z
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    distance = (dx**2 + dy**2 + dz**2)**.5
    return distance


class Line(GeometryBase):
    """This class inherits GeometryBase"""
    def __init__(self, start_point, end_point):
        self.StartPoint = start_point
        self.EndPoint = end_point
        self.Length = None
        self.calc_length()

    def calc_length(self):
        dist = point_distance(self.StartPoint, self.EndPoint)
        self.Length = dist


class Point3d(GeometryBase):
    """This class inherits GeometryBase"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coordinates = [x, y, z]


def main():
    start_point = Point3d(20, 50, 0)
    end_point = Point3d(10, 0, 300)
    line = Line(start_point, end_point)
    print(line.Length)


if __name__ == "__main__":
    main()


