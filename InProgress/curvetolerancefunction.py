import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg

doc = Rhino.RhinoDoc.ActiveDoc



#select and hide all line-like curves
curves = rs.GetObjects("select curves")
for curve in curves:
    guid = curve
    obj = doc.Objects.Find(guid)
    geo = obj.Geometry
    if geo.IsLinear():
        rs.HideObject(curve)
    

#automate bringing tolerance down to .005 recursively through list


    """
#rs.RebuildCurve()
rebuilds = []
for curve in curves:
    copy = rs.CopyObject(curve)
    for i in range(4,30,1):
        rs.RebuildCurve(curve, point_count=i)
        rebuild_copy = rs.CopyObject(curve)
        dev = rs.CurveDeviation(copy, curve)
        print dev[1]

"""