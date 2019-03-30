import rhinoscriptsyntax as rs


for i in range(200):
    point = rs.GetPoint("Select Point")
    txt = "x"
    
    rs.AddTextDot(txt, point)