import rhinoscriptsyntax as rs


blocks = rs.GetObjects("Select Text Blocks")

rs.EnableRedraw(False)

for b in blocks:
    name = rs.BlockInstanceName(b)
    point = rs.BlockInstanceInsertPoint(b)
    
    text = rs.AddText(name, point, height=1.5, justification=131074)


rs.EnableRedraw(True)
