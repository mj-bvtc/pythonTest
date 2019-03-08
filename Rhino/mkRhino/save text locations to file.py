import rhinoscriptsyntax as rs


text = rs.GetObjects("Select Text", rs.filter.annotation)

file = r"C:\Users\mkreidler\Desktop\textpt.txt"
with open(file, "w+") as f:

    for t in text:
        txt =  t
        pt =  rs.TextObjectPoint(t)
        line = "{},{}\n".format(txt, pt)
        f.write(line)