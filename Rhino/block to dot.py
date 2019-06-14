import rhinoscriptsyntax as rs


blocks = rs.GetObjects("Select Text Blocks")

rs.EnableRedraw(False)

for b in blocks:
    name = rs.BlockInstanceName(b)
    point = rs.BlockInstanceInsertPoint(b)
    
    text = rs.AddTextDot(name, point)


rs.EnableRedraw(True)
