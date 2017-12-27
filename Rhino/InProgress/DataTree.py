import rhinoscriptsyntax as rs
import Rhino
import uuid
import datetime

"""
class block:
    def __init__(self, pt, name):
        self.id = uuid.uuid4()
        self.pt = pt
        self.name = name
    def add_name(self):
        rs.AddText(self.name, self.pt)


pt = rs.coerce3dpoint(rs.GetObject())
name = "A"

a = block(pt, name)
a.add_name()


point = rs.coerce3dpoint(rs.GetObject())
curve = rs.coercecurve(rs.GetObject())
is_in = rs.PointInPlanarClosedCurve(point, curve)

print is_in
"""

class block:
    def __init__(self, name=None):
        self.name = name
        self.datetime = datetime.datetime.now()
        self.id = uuid.uuid4()
        self.name = name
        self.point = None
        self.block = None
    def add_pt(self):
       pt =  rs.AddPoint(rs.GetPoint("Select point"))
       self.point = pt
    def get_name(self):
        self.name = raw_input("Type in name").upper()
    def assign_block(self):
        if (self.name != None) & (self.point != None):
            text = rs.AddText(self.name, self.point, justification=131074)
            self.block = rs.AddBlock([text], self.point, self.name)
    def make(self):
        self.add_pt()
        self.get_name()
        self.assign_block()

b = block()
b.make()