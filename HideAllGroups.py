import rhinoscriptsyntax as rs

names = rs.GroupNames()
for group in names:
    rs.HideGroup(group)

rs.Redraw()