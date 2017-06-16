import DynamicPlane
import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


doc = Rhino.RhinoDoc.ActiveDoc

def max_view(name):
    rs.CurrentView(name)
    Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.Maximized = True
    rs.ZoomExtents(None, True)




def main():
    #initial set up
    max_view("Perspective")
    rs.ZoomExtents(None, True)
    mesh = rs.GetObject("Select Mesh", filter = rs.filter.mesh)
    rs.OsnapMode(64)
    rs.Osnap(True)
    

    
    start, origin, x, y= DynamicPlane.DynamicPlane()
    end = rg.Plane(rg.Point3d.Origin, rg.Vector3d.XAxis, rg.Vector3d.ZAxis)
    factor = 8/origin.DistanceTo(x)
    scale = rg.Transform.Scale(origin, factor)
    map = rg.Transform.PlaneToPlane(start, end)
    xform = scale * map
    
    rs.TransformObject(mesh, xform, False)
    
    dim = rg.LinearDimension(end, rg.Point2d.Origin, rg.Point2d(8,0), rg.Point2d(4,3))
    

    
    Rhino.RhinoDoc.ActiveDoc.Objects.AddLinearDimension(dim)
    
    max_view("Front")
    rs.Redraw()


if __name__ == "__main__":
    main()