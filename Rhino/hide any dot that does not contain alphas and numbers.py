import rhinoscriptsyntax as rs
import re


rs.EnableRedraw(False)
rs.Command("!_SelNone ")
rs.Command("!_SelDot ")
dots = rs.SelectedObjects()
rs.Command("!_SelNone ")




for d in dots:
    test = rs.TextDotText(d)
    pattern1 = r"[0-9]+"
    pattern2 = r"[a-z]+"
    result1 = bool(re.search(pattern1, test,flags=re.IGNORECASE))
    result2 = bool(re.search(pattern2, test,flags=re.IGNORECASE))
    final = result1 and result2
    
    if final == True:
        rs.HideObject(d)





rs.EnableRedraw(True)