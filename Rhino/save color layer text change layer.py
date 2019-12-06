import rhinoscriptsyntax as rs



dots = rs.GetObjects()


rs.EnableRedraw(False)

for d in dots:
    #save original settings
    color = rs.ObjectColor(d)
    layer = rs.ObjectLayer(d)
    text = rs.TextDotText(d)
    rs.SetUserText(d, "original_color", value=color) 
    rs.SetUserText(d, "original_layer", value=layer) 
    rs.SetUserText(d, "original_text", value=text) 
    
    #change layer    
    rs.ObjectLayer(d, layer="Mickey Adds")
    rs.ObjectColor(d, color=color)

rs.EnableRedraw(True)