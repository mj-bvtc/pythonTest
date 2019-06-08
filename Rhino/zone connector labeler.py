import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg

objs = rs.GetObjects("get objects")

class zone():
    def __init__(self):
        self.dots = []
        self.curves = []
    
    def report(self):
        print len(self.dots)
        print len(self.curves)





z = zone()
a = Rhino.RhinoDoc.ActiveDoc.Objects.Find(o)
print type(a)
if type(a) == Rhino.DocObjects.TextDotObject:
    print "dot"
    z.dots.append(o)
if type(a) == Rhino.DocObjects.CurveObject:
    print "curve"
    z.curves.append(o)
z.report()


#Rhino.RhinoDoc.ActiveDoc.Objects.Find(o)