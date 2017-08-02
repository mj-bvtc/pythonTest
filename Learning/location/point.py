import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def distance_to_origin(self):
        xy = self.pythagorean_theorem(self.x, self.y)
        xyz = self.pythagorean_theorem(xy, self.z)
        return xyz

    @staticmethod
    def pythagorean_theorem(a, b):
        c = math.sqrt(a**2 + b**2)
        return c

    def distance_to_point(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        dz = abs(self.z - other.z)
        dxdy = self.pythagorean_theorem(dx, dy)
        dxdydz = self.pythagorean_theorem(dxdy, dz)
        return dxdydz


a = Point(1, 2, 3)
b = Point(6, 5, -3)

print(b.distance_to_point(a))
