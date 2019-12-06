import rhinoscriptsyntax as rs
import Rhino


def find_bigger_groups():
    groups = rs.GroupNames()
    
    for g in groups:
        objects = rs.ObjectsByGroup(g, select=False)
        num = len(objects)
        if num>2:
            print g

"""
Group107
Group108
Group109
Group110
Group111
Group113
Group393
Group739
"""

def sel_group(name):
    objects = rs.ObjectsByGroup(name, select=False)
    print objects
    #rs.SelectObjects(objects)
    #rs.ZoomSelected()




#sel_group("Group108")




def hide_small():
    rs.EnableRedraw(False)
    groups = rs.GroupNames()
    
    for g in groups:
        objects = rs.ObjectsByGroup(g, select=False)
        num = len(objects)
        if num<=2:
            rs.HideGroup(g)
    rs.EnableRedraw(True)

hide_small()