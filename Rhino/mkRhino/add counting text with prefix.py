import rhinoscriptsyntax as rs


for i in range(21):
    i+=1
    txt = "W1-{}".format(i)
    pt = rs.GetPoint("Select point")
    rs.AddText(txt, pt, height=11.6)
    