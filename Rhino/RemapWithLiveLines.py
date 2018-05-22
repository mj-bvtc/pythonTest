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
    mesh = rs.GetObjects("Select Objects")
    rs.OsnapMode(64)
    rs.Osnap(True)
    
    #initial, rough orientation
    start, origin, x, y= DynamicPlane.DynamicPlane()
    end = rg.Plane(rg.Point3d.Origin, rg.Vector3d.XAxis, rg.Vector3d.ZAxis)
    map = rg.Transform.PlaneToPlane(start, end)
    rs.TransformObject(mesh, map, False)
    max_view("Front")
    

    max_view("Perspective")
    rs.Command("'_CPlane _World _Top") ##############testing this
    max_view("Front")
    rs.ViewCPlane(None, end)
    rs.Redraw()
    


if __name__ == "__main__":
    main()