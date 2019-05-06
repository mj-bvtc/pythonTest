import rhinoscriptsyntax as rs


obs = rs.GetObjects("sel blocks")
area = raw_input("Type in prefix")

rs.EnableRedraw(False)

for i,o in enumerate(obs):
    i += 1
    msg = "{}-{}".format(area, i)
    label = rs.TextDotText(o, text=msg)
    #rs.HideObject(o)
    rs.ObjectLayer(o,layer="Relabeled")
    
    
    
rs.EnableRedraw(True)