import rhinoscriptsyntax as rs

obs = rs.GetObjects("Select Text Objects", filter=rs.filter.annotation )

name = raw_input("Type name to assign")

rs.EnableRedraw(enable=False)

for o in obs:
    
    txt = rs.TextObjectText(o)
    pt = rs.TextObjectPoint(o)
    rs.AddTextDot(txt, pt)
    rs.TextObjectText(o,name)
    

rs.EnableRedraw(enable=True)