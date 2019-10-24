import rhinoscriptsyntax as rs
import Rhino

def dupface():
    brep = rs.GetObject()
    rs.HideObject(brep)
    exploded = rs.ExplodePolysurfaces(brep)
    face = rs.GetObject()
    border = rs.DuplicateSurfaceBorder(face)
    
    delete = [exploded, face]
    rs.DeleteObjects(delete)
    rs.ShowObject(brep)
    
    print border
    

crv = rs.GetObject()
centroid = rs.CurveAreaCentroid(crv)[0]
dist = .25

rs.OffsetCurve(crv, centroid, dist)

