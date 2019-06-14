import rhinoscriptsyntax as rs


obs = rs.GetObjects("sel zones")
area = raw_input("Type in prefix")

#rs.EnableRedraw(False)

for i,o in enumerate(obs):
    i += 1
    msg = "{}{}".format(area, i)
    #label = rs.BlockInstanceName(o)
    point = rs.GetPoint()
    dot = rs.AddTextDot(msg, point)
    #rs.HideObject(o)
    #rs.ObjectLayer(o,layer="Relabeled")
    
    
    
#rs.EnableRedraw(True)