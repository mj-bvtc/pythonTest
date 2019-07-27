import rhinoscriptsyntax as rs

dots = rs.GetObjects()

rs.EnableRedraw(False)
for d in dots:
    original = rs.TextDotText(d)
    new_name = original.replace(",", "--")
    rs.TextDotText(d, text=new_name)
rs.EnableRedraw(True)


