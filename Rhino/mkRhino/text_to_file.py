import rhinoscriptsyntax as rs

with open(r"C:\Users\mkreidler\Desktop\51w81st_2.txt", "w") as f:
    
    f.write("name,guid\n")
    objs = rs.GetObjects()
    for o in objs:
        
        name = rs.TextObjectText(o)
        guid = o
        msg = "{},{}\n".format(name, guid)
        f.write(msg)
        
        
        