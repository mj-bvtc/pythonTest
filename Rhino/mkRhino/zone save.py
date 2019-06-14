import rhinoscriptsyntax as rs

entries = []
entries.append("name,dot,zone\n")

zones = rs.GetObjects("Sel Closed crvs")
num = len(zones)
print num

for i in range(num):
    dot = rs.GetObject("Select Dot", filter = rs.filter.textdot)
    zone = rs.GetObject("Select Zone", filter= rs.filter.curve)
    name = rs.TextDotText(dot)
    
    rs.HideObject(dot)
    rs.HideObject(zone)
    
    entry = "{},{},{}\n".format(name,dot,zone)
    entries.append(entry)

with open(r"C:\Users\mkreidler\Desktop\100 Huson Zone.txt", "w+") as f:
    for e in entries:
        f.write(e)



