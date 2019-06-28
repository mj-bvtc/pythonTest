import rhinoscriptsyntax as rs


points = rs.GetObjects()

rs.EnableRedraw(False)

for p in points:
    text = "X"
    t = rs.AddText(text, p, justification=131074)

    
    if text in rs.BlockNames():
        block = rs.InsertBlock(text, p)
        #rs.ObjectLayer(block, layer=layer)
        #rs.DeleteObject(o)
        
    else:
        
        
    
    
        block_def = rs.AddBlock([t], p, name=text, delete_input=False)
        block = rs.InsertBlock(text, p)
        #rs.ObjectLayer(block, layer=layer)

rs.EnableRedraw(True)