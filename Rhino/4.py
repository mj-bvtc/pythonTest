import rhinoscriptsyntax as rs


dots = rs.GetObjects()

dots = sorted(list(set([rs.TextDotText(d) for d in dots])))

for d in dots:
    if d.isalnum():
        pass
    else:
        print d