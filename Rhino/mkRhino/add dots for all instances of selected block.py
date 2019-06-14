import rhinoscriptsyntax as rs


#rs.BlockInstanceName()

#rs.BlockContainerCount()

def dot_blocks(block):
    name = rs.BlockInstanceName(block)
    blocks = rs.BlockInstances(name)
    
    for b in blocks:
        
        point = rs.BlockInstanceInsertPoint(b)
        text = name
        dot = rs.AddTextDot(text, point)
    
#dot_blocks()

def dot_lots_blocks():
    blocks = rs.GetObjects("Select block instances to dot")
    rs.EnableRedraw(False)
    for b in blocks:
        dot_blocks(b)
    rs.EnableRedraw(True)

dot_lots_blocks()
