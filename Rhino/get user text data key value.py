import rhinoscriptsyntax as rs

obj = rs.GetObject("Select object")
if obj:
    results = rs.GetUserText(obj)
    for r in results:
        print r, rs.GetUserText(obj, r)


