import Rhino
import rhinoscriptsyntax as rs

origin = rs.GetPoint("Get origin")
rs.AddPoint(origin)
x_pt = rs.GetPoint("Get X Point")
rs.AddLine(origin, x_pt)


normal = Rhino.Geometry.Vector3d(x_pt - origin)
plane = Rhino.Geometry.Plane(origin, normal)

closest_y_pt = rs.GetPoint("Get Y Point")


y_pt = plane.ClosestPoint(closest_y_pt)


radius = origin.DistanceTo(y_pt)
circle = Rhino.Geometry.Circle(plane, radius)
Rhino.RhinoDoc.ActiveDoc.Objects.AddCircle(circle)

rs.AddPoint(y_pt)

