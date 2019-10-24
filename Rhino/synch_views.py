import rhinoscriptsyntax as rs


existing_views = set(rs.ViewNames())
intended_views = {"Top", "Perspective", "Front","Right", "Left", "Back", "Bottom"}

to_add = intended_views - existing_views

for t in to_add:
    rs.Command("!_NewViewport {} ".format(t))

for v in rs.ViewNames():
    rs.ViewDisplayMode(view=v, mode="Rendered")
    
    
