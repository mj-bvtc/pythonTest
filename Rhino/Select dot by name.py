import rhinoscriptsyntax as rs

rs.Command("_SelDot ")
objs = rs.SelectedObjects()
rs.Command("_SelNone")

rs.EnableRedraw(False)
for o in objs:
    text = rs.TextDotText(o)
    if text == "SF1":
        rs.SelectObject(o)
rs.EnableRedraw(True)

