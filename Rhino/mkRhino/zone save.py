import rhinoscriptsyntax as rs

entries = []
entries.append("name,dot,zone\n")

for i in range(38):
    dot = rs.GetObject("Select Dot", filter = rs.filter.textdot)
    zone = rs.GetObject("Select Zone", filter= rs.filter.curve)
    name = rs.TextDotText(dot)
    
    rs.HideObject(dot)
    rs.HideObject(zone)
    
    entry = "{},{},{}\n".format(name,dot,zone)
    entries.append(entry)

with open(r"V:\Projects\PS 171M_P18-1593\TerraCotta\_Preliminary_Models\_archive\zones.txt", "w+") as f:
    for e in entries:
        f.write(e)



