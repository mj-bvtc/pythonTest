import rhinoscriptsyntax as rs
import rhinoscriptsyntax as rs
import random
import time
import Rhino
import uuid 



def rand_color():
    r = lambda: random.randint(0,255)
    color = [r(),r(),r()]
    return color


class Group():
    def __init__(self):
        self.guid = None
        self.color = None
        self.name = None



def apply_colors():
    rs.EnableRedraw(False)
    rs.Command("_SelNone")
    rs.Command("_SelDot")
    dots = rs.SelectedObjects()
    
    names = set()
    groups = []
    
    for d in dots:
        g = Group()
        g.guid = d
        name = rs.TextDotText(d)
        g.name = name
        names.add(name)
        groups.append(g)
    
    for name in names:
        color = rand_color()
        for g in groups:
            if g.name == name:
                g.color = color
                rs.ObjectColor(g.guid, color=color)
    
    rs.Command("_SelNone")
    rs.EnableRedraw(True)

apply_colors()