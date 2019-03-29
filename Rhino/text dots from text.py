import rhinoscriptsyntax as rs


obs = rs.GetObjects("Select all text")

rs.EnableRedraw(enable=False)

for ob in obs:
    txt = rs.TextObjectText(ob)
    print txt
    pt = rs.TextObjectPoint(ob)
    print pt
    #dot = rs.AddTextDot(txt, pt)
    print 
    print


rs.EnableRedraw(enable=True)