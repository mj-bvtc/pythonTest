import rhinoscriptsyntax as rs
import rhinoscriptsyntax as rs
import random
import time
import Rhino
import uuid 



def rand_color():
    r = lambda: random.randint(0,255)
    color = [r(),r(),r()]
    return color

#rs.BlockInstanceName()

#rs.BlockContainerCount()

def dot_blocks(block, color=None, profile=None):
    name = rs.BlockInstanceName(block)
    blocks = rs.BlockInstances(name)
    
    for b in blocks:
        
        point = rs.BlockInstanceInsertPoint(b)

        text = name
        dot = rs.AddTextDot(text, point)
        if profile:
            rs.ObjectName(dot, profile)
        if color:
            rs.ObjectColor(dot, color=color)
            #rs.ObjectColorSource(dot, 1) ##object source is object
        rs.HideObject(dot)
    rs.HideObjects(blocks)

    
#dot_blocks()

def dot_lots_blocks():
    blocks = rs.GetObjects("Select block instances to dot")
    rs.EnableRedraw(False)
    color1 = rand_color()
    print color1
    profile = str(uuid.uuid4())
    for b in blocks:
        
        dot_blocks(b, color=color1, profile = profile)
    rs.HideObjects(blocks)
    rs.EnableRedraw(True)

dot_lots_blocks()
