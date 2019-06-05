import rhinoscriptsyntax as rs

name = raw_input("Type in the name to apply")

texts = rs.GetObjects("Select text objects to apply to", filter=rs.filter.textdot)

rs.EnableRedraw(False)

for t in texts:
    rs.TextDotText(t, name)

rs.EnableRedraw(True)