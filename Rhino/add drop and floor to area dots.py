import rhinoscriptsyntax as rs

points = []
texts = []

rs.EnableRedraw(False)
rs.Command("_SelNone ")
rs.Command("_SelDot ")
dots = rs.SelectedObjects()
rs.Command("_SelNone ")
for d in dots:
    text = rs.TextDotText(d)
    texts.append(text)
    point = rs.TextDotPoint(d)
    points.append(point)


rs.Command("_SelNone ")
rs.Command("_SelClosedCrv ")
zones = rs.SelectedObjects()
rs.Command("_SelNone ")


newNames = []

for i,d in enumerate(dots):
    
    drop = None
    floor = None
    
    results = []
    
    # get containment zones
    for z in zones:
        p = rs.TextDotPoint(d)
        test = rs.PointInPlanarClosedCurve(p, z)
        if test == 1:
                results.append(z)
    #print len(results)
    # test for floor/drop
    
    for r in results:
        name = rs.ObjectName(r)
        if "FLOOR" in name:
            floor = name.replace("FLOOR ", "")
        if "DROP" in name:
            drop = name.replace("DROP ", "")
    
    new_text = texts[i] + " (" + drop + "-" + floor + ")"
    #print new_text
    rs.TextDotText(d, text=new_text)

rs.EnableRedraw(True)

