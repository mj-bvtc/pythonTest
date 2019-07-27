import rhinoscriptsyntax as rs
import re

rs.EnableRedraw(False)
rs.Command("!_SelNone ")
rs.Command("!_SelDot ")
dots = rs.SelectedObjects()
rs.Command("!_SelNone ")

for d in dots:
    name = rs.TextDotText(d)
    x,y,z = rs.TextDotPoint(d)
    if " " in name:
        pattern = r"\b\w[\S]*"
        results = re.findall(pattern, name,flags=re.IGNORECASE)
        rs.DeleteObject(d)
        for i,word in enumerate(results):
            if i == 0:
                x += .074
                point = [x,y,z]
                rs.AddTextDot(word, point)
            else:
                x += .162
                point = [x,y,z]
                rs.AddTextDot(word, point)
    else:
        rs.HideObject(d)



rs.EnableRedraw(True)