import rhinoscriptsyntax as rs
import re


text = rs.GetObjects()

rs.EnableRedraw(False)
for t in text:
    if  rs.TextObjectText(t).isdigit():
        rs.DeleteObject(t)
rs.EnableRedraw(True)
