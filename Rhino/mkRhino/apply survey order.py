import rhinoscriptsyntax as rs

with open(r"C:\Users\mkreidler\Desktop\surveyorder6.txt", "r") as f:
    
    content =f.readlines()
    content = [x.strip() for x in content] 
    
    rs.EnableRedraw(False)
    
    for line in content:
        guid,num = line.split(",")
        pt = rs.TextObjectPoint(guid)
        txt = rs.TextObjectText(guid)
        #layer = rs.ObjectLayer(guid)
        color = rs.ObjectColor(guid)
        info = "#{} ({})".format(str(num), txt)
        dot = rs.AddTextDot(info, pt)
        rs.ObjectColor(dot, color)
    
    
    rs.EnableRedraw(True)