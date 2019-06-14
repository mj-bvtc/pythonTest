import rhinoscriptsyntax as rs

file = r"C:\Users\mkreidler\Desktop\ps171animation.txt"
content = []
with open(file, "r") as f:
    content = f.readlines()
    content = [x.strip() for x in content] 

for i,c in enumerate(content):
    rs.SelectObject(c)
    rs.ZoomSelected()


    #rs.UnselectAllObjects() 
    if i == 20:
        break









