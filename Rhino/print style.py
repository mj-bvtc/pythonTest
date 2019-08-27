import rhinoscriptsyntax as rs


rs.Command("_SelNone ")
rs.Command("_SelBlockInstance ")
objs = rs.SelectedObjects()
rs.Command("_SelNone ")

rs.EnableRedraw(False)
for o in objs:
    style = rs.GetUserText(o, key="style")
    print style
rs.EnableRedraw(True)