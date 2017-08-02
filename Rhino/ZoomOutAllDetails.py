import rhinoscriptsyntax as rs
import Rhino
import time

doc = Rhino.RhinoDoc.ActiveDoc

def main():
    views = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.GetDetailViews()
    
    
    detail_ids = [x.Id for x in views]
    
    for detail in detail_ids:
        doc.Views.ActiveView.SetActiveDetail(detail)
        rs.Command("_Zoom Out")
        #rs.ZoomExtents()
        #time.sleep(1)
        Rhino.RhinoApp.Wait()
    
    rs.Redraw()

if __name__ == "__main__":
    main()
