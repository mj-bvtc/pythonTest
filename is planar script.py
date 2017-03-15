import rhinoscriptsyntax as rs
import Rhino
doc = Rhino.RhinoDoc.ActiveDoc

srf = rs.GetSurfaceObject("select surface")
tol = rs.UnitAbsoluteTolerance()
guid = srf[0]
obj = doc.Objects.Find(guid)
geo = obj.Geometry.Surfaces[0]


is_planar = geo.IsPlanar(tol)

if is_planar:
    print "This surface is planar"
else:
    print "This surface is not planar"


