import rhinoscriptsyntax as rs


rs.EnableRedraw(False)

views = rs.ViewNames()

for view in views:

    rs.ViewDisplayMode(view, 'Rendered')

rs.EnableRedraw(True)