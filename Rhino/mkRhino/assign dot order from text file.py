import rhinoscriptsyntax as rs


file = r"C:\Users\mkreidler\Desktop\number_guids.txt"

rs.EnableRedraw(False)

with open(file, "r") as f:
    content = f.readlines()
    content = [x.strip() for x in content] 
    for i, line in enumerate(content):
        i += 1
        point = rs.TextDotPoint(line)
        dot = rs.AddTextDot(i, point)
        


rs.EnableRedraw(True)