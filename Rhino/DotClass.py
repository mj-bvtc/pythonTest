import rhinoscriptsyntax as rs
import Rhino
import time
import random


doc = Rhino.RhinoDoc.ActiveDoc

class Count:
    def __init__(self, name=""):
        self.dots = []
        self.points = []
        self.line = None
        self.name = name

    @property
    def count(self):
        return len(self.points)

    def get_point(self):
        point = rs.GetPoint("Select Point")
        self.points.append(point)
        return point

    def get_points(self, num):
        for get in range(num):
            self.get_point()

    def add_dots(self):
        for point in self.points:
            dot = rs.AddTextDot(self.name, point)
            self.dots.append(dot)
        return
    
    def save_points(self, file):
        text = open(file, "w")
        for point in self.points:
            coord = point.ToString()
            text.write(coord + "\n")
        text.close()
    
    def read_points(self, path):
        file = open(path, "r")
        for line in file:
            self.points.append(line)
        file.close()

def random_point(low=-28000, hi=28000):
    x = random.randint(low, hi)
    y = random.randint(low, hi)
    z = random.randint(low, hi)
    return x,y,z

def random_points(number):
    points = []
    for point in range(number):
        points.append(random_point())
    return points

def random_letter():
    alpha = list("abcdefghijklmnopqrstuvwxyz")
    return random.choice(alpha)

def random_name():
    num = str(random.randint(1, 50))
    return random_letter() + num

rs.EnableRedraw(False)

objs = [Count() for i in range(500)]
for obj in objs:
    obj.name = random_name()
    obj.points.append(random_point())
    obj.add_dots()

rs.EnableRedraw(True)


"""

rs.EnableRedraw(False)
c = Count("A34")
#c.get_points(5)
c.read_points(r"C:\Users\mkreidler\Desktop\points.txt")
c.add_dots()
#c.get_points(200)
#c.save_points(r"C:\Users\mkreidler\Desktop\points.txt")
rs.EnableRedraw(True)

print c.count

"""
print "script finished"

