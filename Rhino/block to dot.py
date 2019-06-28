import rhinoscriptsyntax as rs


blocks = rs.GetObjects("Select Text Blocks")

rs.EnableRedraw(False)

for b in blocks:
    name = rs.BlockInstanceName(b)
    point = rs.BlockInstanceInsertPoint(b)
    layer = rs.ObjectLayer(b)
    
    
    text = rs.AddTextDot(name, point)
    rs.ObjectLayer(text, layer=layer)


rs.EnableRedraw(True)
