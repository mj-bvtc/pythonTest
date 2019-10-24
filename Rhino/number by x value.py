import rhinoscriptsyntax as rs


dots = rs.GetObjects()
x_vals = []

for d in dots:
    x = rs.TextDotPoint(d)[0]
    x_vals.append(x)
    
    
    
    
zipped = zip(x_vals, dots)

res = sorted(zipped, key = lambda x: x[0]) 

rs.EnableRedraw(False)
for i,r in enumerate(res):
    num = i + 1
    x = r[0]
    dot = r[1]
    rs.TextDotText(dot, text=str(num))
    color = rs.ObjectColor(dot)
    rs.ObjectColor(dot, color=color)

rs.EnableRedraw(True)