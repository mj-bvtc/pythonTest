import rhinoscriptsyntax as rs

word = "DROP "

dots = rs.GetObjects()

rs.EnableRedraw(False)

for d in dots:
    text = rs.TextDotText(d)
    prefixed = word + text
    rs.TextDotText(d, text=prefixed)



rs.EnableRedraw(True)


