import rhinoscriptsyntax as rs


for i in range(1,30):
    pt = rs.GetPoint()
    rs.AddText(i, pt, height=.619, justification=131074)