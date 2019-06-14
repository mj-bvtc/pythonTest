import rhinoscriptsyntax as rs


objs = rs.GetObjects()
prefix = "PRIORITY "
for o in objs:
    crv = rs.GetObject("Select zone")
    name = raw_input("Type in name of zone")
    name = prefix + name
    rs.ObjectName(crv, name=name)
    rs.HideObject(crv)