import rhinoscriptsyntax as rs


objs = rs.GetObjects(filter=rs.filter.textdot)

rs.EnableRedraw(False)


for o in objs:
    name = rs.TextDotText(o)
    point = rs.TextDotPoint(o)
    layer = rs.ObjectLayer(o)
    
    if name in rs.BlockNames():
        block = rs.InsertBlock(name, point)
        rs.ObjectLayer(block, layer=layer)
        rs.ObjectName(o, name=name)
        #rs.DeleteObject(o)
        
    else:
        
        
    
    
        block_def = rs.AddBlock([o], point, name=name, delete_input=False)
        block = rs.InsertBlock(name, point)
        rs.ObjectName(o, name=name)
        rs.ObjectLayer(block, layer=layer)


rs.EnableRedraw(True)


