import rhinoscriptsyntax as rs

entries = []
entries.append("name,dot,zone\n")

for i in range(1):
    dot = rs.GetObject("Select Dot", filter = rs.filter.textdot)
    zone = rs.GetObject("Select Zone", filter= rs.filter.curve)
    name = rs.TextDotText(dot)
    
    entry = "{},{},{}\n".format(name,dot,zone)
    entries.append(entry)

with open(r"C:\Users\mkreidler\Desktop\zones.txt", "w+") as f:
    for e in entries:
        f.write(e)



