import rhinoscriptsyntax as rs


txt = r"C:\Users\mkreidler\Desktop\ps171_survey.txt"

rs.EnableRedraw(False)

with open(txt, "r") as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    
    for c in content:
        name, guid, num = c.split(",")
        point = rs.TextObjectPoint(guid)
        rs.AddTextDot(str(num), point)
        #print guid


rs.EnableRedraw(True)

