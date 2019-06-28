import rhinoscriptsyntax as rs

rs.Command("_SelDot")
objs=rs.SelectedObjects()

rs.EnableRedraw(False)
for o in objs:
    name = rs.TextDotText(o)
    if name not in ["Z", "H1"]:
        rs.HideObject(o)
rs.Command("_SelNone")
rs.EnableRedraw(True)