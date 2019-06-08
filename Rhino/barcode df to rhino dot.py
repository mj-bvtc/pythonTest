import rhinoscriptsyntax as rs


file = r"C:\Users\mkreidler\Desktop\new100Hudson_label barcode dots2.txt"

content = []

with open(file, "r") as f:
    
    content = f.readlines()
    content = [x.strip() for x in content] 


rs.EnableRedraw(False)

for row in content:
    guid,name =  row.split(",")
    guid = guid.strip()
    name = name.strip()
    name = name.split("[")[1].replace("]","")
    point = rs.BlockInstanceInsertPoint(guid)
    rs.AddTextDot(name, point)

rs.EnableRedraw(True)