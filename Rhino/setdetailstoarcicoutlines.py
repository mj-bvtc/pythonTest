import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def SetDetailsToArcticOutlines():
    display_mode = Rhino.Display.DisplayModeDescription.FindByName("Arctic With Outlines")
    if display_mode:
        page_views = sc.doc.Views.GetPageViews()
        for page_view in page_views:
            details = page_view.GetDetailViews()
            for detail in details:
                if detail.Viewport.DisplayMode.Id != display_mode.Id:
                    detail.Viewport.DisplayMode = display_mode
                    detail.CommitViewportChanges()
            page_view.Redraw()


SetDetailsToArcticOutlines()