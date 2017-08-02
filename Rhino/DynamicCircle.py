# A Rhino GetPoint that performs some custom dynamic drawing
import Rhino
import System.Drawing.Color
import scriptcontext

def DynamicPlane():
    # Color to use when drawing dynamic lines
    line_color = System.Drawing.Color.FromArgb(255,0,0)
    circle_color = System.Drawing.Color.FromArgb(150,0,50)


    rc, origin = Rhino.Input.RhinoGet.GetPoint("Select Origin point", False)
    if( rc!=Rhino.Commands.Result.Success ): return

    rc, x_pt = Rhino.Input.RhinoGet.GetPoint("Select X point", False)
    if( rc!=Rhino.Commands.Result.Success ): return
        
        
    normal = Rhino.Geometry.Vector3d(x_pt - origin)
    plane = Rhino.Geometry.Plane(origin, normal)
    


    # This is a function that is called whenever the GetPoint's
    # DynamicDraw event occurs
    def DynamicCircle( sender, args ):
        
        
        
        
        closest_y_pt = args.CurrentPoint
        y_pt = plane.ClosestPoint(closest_y_pt)
        
        
        
        
        #dynamic line from origin to y_pt
        args.Display.DrawLine(origin, y_pt, line_color, 2)

        radius = origin.DistanceTo(y_pt)
        #draw an circle through these three points
        circle = Rhino.Geometry.Circle(plane, radius)
        args.Display.DrawCircle(circle, circle_color, 1)
        

    # Create an instance of a GetPoint class and add a delegate
    # for the DynamicDraw event
    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += DynamicCircle
    gp.Get()
    if( gp.CommandResult() == Rhino.Commands.Result.Success ):
        pt = gp.Point()

        scriptcontext.doc.Views.Redraw()


if( __name__ == "__main__" ):
    DynamicPlane()