# A Rhino GetPoint that performs some custom dynamic drawing
import Rhino
import System.Drawing.Color
import scriptcontext

def DynamicLine():
    # Color to use when drawing dynamic lines
    line_color = System.Drawing.Color.FromArgb(255,0,0)


    rc, origin = Rhino.Input.RhinoGet.GetPoint("Select Origin point", False)
    if( rc!=Rhino.Commands.Result.Success ): return

    # This is a function that is called whenever the GetPoint's
    # DynamicDraw event occurs
    def Dynamic( sender, args ):
        
        args.Display.DrawLine(origin, args.CurrentPoint, line_color, 2)

    # Create an instance of a GetPoint class and add a delegate
    # for the DynamicDraw event
    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += Dynamic
    gp.Get()
    if( gp.CommandResult() == Rhino.Commands.Result.Success ):
        pt = gp.Point()
        #Rhino.RhinoDoc.ActiveDoc.Objects.AddPoint(pt)
        #Rhino.RhinoDoc.ActiveDoc.Objects.AddPoint(origin)

        scriptcontext.doc.Views.Redraw()
        return origin, pt


if( __name__ == "__main__" ):
    DynamicLine()