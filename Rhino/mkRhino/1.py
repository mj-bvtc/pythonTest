import rhinoscriptsyntax as rs

obs = rs.GetObjects()

for o in obs:
    text = rs.TextDotText(o)
    new_text = "DROP " + text
    rs.TextDotText(o, text=new_text)
