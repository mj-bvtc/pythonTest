import rhinoscriptsyntax as rs


texts = rs.GetObjects()
to_print = []

for t in texts:
    msg = rs.TextObjectText(t)
    to_print.append(msg)


result = sorted(to_print)

for r in result:
    print r