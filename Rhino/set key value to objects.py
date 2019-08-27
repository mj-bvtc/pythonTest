import rhinoscriptsyntax as rs


def set_key_value():
    objs = rs.GetObjects()
    if objs:
        key = raw_input("Key ")
        val = raw_input("Value ")
        
        for o in objs:
            rs.SetUserText(o, key, value=val)

def set_value(key):
    val = raw_input("Value ")
    objs = rs.GetObjects()
    if objs:
        
        
        for o in objs:
            rs.SetUserText(o, key, value=val)

dots = rs.GetObjects()

rs.EnableRedraw(False)
for d in dots:
    style = rs.TextDotText(d)
    rs.SetUserText(d, key="style", value=style)
rs.EnableRedraw(True)