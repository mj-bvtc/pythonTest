import rhinoscriptsyntax as rs


for i in range(200):
    point = rs.GetPoint("get pt")
    text = "X"
    rs.AddTextDot(text, point)
    print i
