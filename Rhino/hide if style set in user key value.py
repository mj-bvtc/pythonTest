import rhinoscriptsyntax as rs


#objs = rs.GetObjects()

rs.Command("_SelNone ")
rs.Command("_SelBlockInstance ")
objs = rs.SelectedObjects()
rs.Command("_SelNone ")

rs.EnableRedraw(False)
for o in objs:
    style = rs.GetUserText(o, key="style")
    if style:
        if style.isalnum():
            rs.HideObject(o)
rs.EnableRedraw(True)