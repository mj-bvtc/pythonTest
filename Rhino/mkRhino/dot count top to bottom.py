import rhinoscriptsyntax as rs

dots = rs.GetObjects("get dots")

class block:
    def __init__(self):
        self.guid = None
        self.z = None
        self.sort_num = None

blocks = []

for d in dots:
    b = block()
    x,y,z = rs.BlockInstanceInsertPoint(d)
    b.y = y
    b.guid = d
    blocks.append(b)

blocks.sort(key=lambda x: x.y, reverse=True)

rs.EnableRedraw(False)

for i,b in enumerate(blocks):
    i += 1
    b.sort_num = i
    rs.BlockInstanceName(b.guid, b.sort_num)
    

rs.EnableRedraw(True)