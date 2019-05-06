import rhinoscriptsyntax as rs

objects = rs.GetObjects("Select Text", rs.filter.annotation)

rs.EnableRedraw(False)

for obj in objects:
    txt = "(" + rs.TextObjectText(obj) +")"
    rs.ObjectName(obj, name=txt)
    

rs.EnableRedraw(True)