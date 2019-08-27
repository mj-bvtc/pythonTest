import rhinoscriptsyntax as rs


text = rs.GetObjects()

rs.EnableRedraw(False)
for t in text:
    tx = rs.TextObjectText(t).upper()
    if "T2" in tx:
        point = rs.TextObjectPoint(t)
        txt = rs.TextObjectText(t)
        rs.AddTextDot(txt, point)
        
rs.EnableRedraw(True)