import rhinoscriptsyntax as rs
import Rhino

def add_hatch_box():
    plane = rs.WorldXYPlane()
    pt1 = rs.GetPoint("select bottom left corner")
    pt2 = rs.GetPoint()
    x,y,z = pt1
    x2,y2,z2 = pt2
    width = abs(x-x2)
    height = abs(y-y2)
    rec = rs.AddRectangle(plane, width, height)
    translation = Rhino.Geometry.Vector3d(pt1)
    rs.MoveObject(rec, translation)
    rs.AddHatch(rec, hatch_pattern="Solid")

for i in range(200):
    add_hatch_box()
