import rhinoscriptsyntax as rs

#this is a note fore ashwini

#select all objects
txt = rs.GetObjects(message="Ashwini! select text", filter=rs.filter.annotation)

for t in txt:
    id = t
    text = rs.TextObjectText(t)
    msg = "{},{}".format(id, text)
    print msg


