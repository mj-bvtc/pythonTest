import rhinoscriptsyntax as rs
import Rhino


def draw_model_paperspace():
    #go to paperspace, then go to view and enter its modelspace
    view = rs.CurrentView()               #rs.CurrentDetail()
    detail = rs.CurrentDetail(view)

    type = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport.ViewportType
    if type != Rhino.Display.ViewportType.DetailViewport:
        print "Please enter detail modelspace"
        return
    print type


    #get model
    objs = rs.GetObjects("Select objects to draw", rs.filter.polysurface)
    rs.SelectObjects(objs)
    
    
    #make 2d, as current view
    rs.Command("!-_Make2D DrawingLayout=CurrentView _enter _enter")
    dwg_crvs = rs.LastCreatedObjects()
    
    
    #cut and paste into view window (paperspace)
    origin = [0,0,0]
    rs.AddBlock(dwg_crvs, origin, name=view, delete_input=True)
    
    
    #leave detail view and insert block
    rs.CurrentDetail(view, detail=view)
    insert_pt = [17,11,0]
    obj = rs.InsertBlock(view, insert_pt)

    #orient 2pt with 3d scaling enabled
    r1 = rs.GetPoint("Pick reference corner 1")
    r2 = rs.GetPoint("Pick reference corner 2")
    t1 = rs.GetPoint("Pick target corner 1")
    t2 = rs.GetPoint("Pick target corner 2")
    ref_pts = [r1, r2]
    target_pts = [t1, t2]
    rs.OrientObject(obj, ref_pts, target_pts, flags=2)
    
    print "Script Finished"
    return 


def main():
    draw_model_paperspace()


if __name__ == "__main__":
    main()