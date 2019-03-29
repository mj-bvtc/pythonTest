import rhinoscriptsyntax as rs

text = rs.GetObjects("Select Text", filter= rs.filter.annotation)

rs.EnableRedraw(False)

for count, t in enumerate(text):
    
    count += 1 
    
    pt = rs.TextObjectPoint(t)
    dot = rs.AddTextDot(count, pt)
    

rs.AddTextDot("Total blocks:  " + str(len(text)), rs.GetPoint("Pick a point for summary dot"))


rs.EnableRedraw(True)