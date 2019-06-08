import rhinoscriptsyntax as rs


objs = rs.GetObjects(filter=rs.filter.annotation)

rs.EnableRedraw(False)


for o in objs:
    name = rs.TextObjectText(o)
    point = rs.TextObjectPoint(o)
    layer = rs.ObjectLayer(o)
    
    if name in rs.BlockNames():
        block = rs.InsertBlock(name, point)
        rs.ObjectLayer(block, layer=layer)
        #rs.DeleteObject(o)
        
    else:
        
        
    
    
        block_def = rs.AddBlock([o], point, name=name, delete_input=False)
        block = rs.InsertBlock(name, point)
        rs.ObjectLayer(block, layer=layer)


rs.EnableRedraw(True)


