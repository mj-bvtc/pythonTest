import rhinoscriptsyntax as rs

obs = rs.GetObjects("Select Dots", filter=rs.filter.textdot)

dots = []

for ob in obs:
    text = rs.TextDotText(ob)
    dots.append(text)
    
    
    

dots.sort()

for d in dots:
    print d