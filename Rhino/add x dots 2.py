import rhinoscriptsyntax as rs

for i in range(100):
    text = "x"
    point = rs.GetPoint()
    rs.AddTextDot(text, point)