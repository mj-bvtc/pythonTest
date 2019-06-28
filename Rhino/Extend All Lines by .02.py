import rhinoscriptsyntax as rs

rs.Command("_SelNone _SelLine ")

objs = rs.SelectedObjects()

rs.EnableRedraw(False)
for o in objs:
    rs.ExtendCurveLength(o, 0, 2, .2) 
rs.EnableRedraw(True)
