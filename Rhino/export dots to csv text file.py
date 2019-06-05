import rhinoscriptsyntax as rs

file = r"C:\Users\mkreidler\Desktop\wolford.txt"

with open(file, "w") as f:
    f.write("guid,name,layer\n")
    dots = rs.GetObjects("get dots")
    for d in dots:
        guid = d
        name = rs.TextDotText(d)
        layer = rs.ObjectLayer(d)
        msg = "{},{},{}\n".format(guid, name, layer)
        f.write(msg)

