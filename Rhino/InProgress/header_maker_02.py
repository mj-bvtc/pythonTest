import rhinoscriptsyntax as rs
import Rhino


class Head:
    """
    A standard TerraCotta Header
    """
    def __init__(self, name, top, bottom):
        self.name = name
        self.top = top
        self.bottom = bottom
        
    def average(self, other, name):
        top = (self.top + other.top)/2
        bottom = (self.bottom + other.bottom)/2
        avg = Head(name, top, bottom)
        return avg

#list all unit measurements
H1L = Head("H1L", 12.875, 15.5)
H2L = Head("H2L", 16.75, 15)
H3 = Head("H3", 16.875, 15)
H2R = Head("H2R", 16.75, 15)
H1R = Head("H1R", 13, 15.5)

heads = (H1L, H2L, H3, H2R, H1R)

#average out the mirrors
H1 = H1L.average(H1R, "H1")
H2 = H2L.average(H2R, "H2")

#define the assembly measurements
class Assembly:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

head_assembly = Assembly("S1-1-HEAD_PORCH", height=13, length=78.75)

#calculate the average mortar gap
def avg_mortar(header_list, assembly):
    count = len(header_list)
    gaps = count - 1 
    top = 0
    bot = 0
    for head in header_list:
        top += head.top
        bot += head.bottom
        
    avg_width= (top + bot)/2
    
    leftover = assembly.length - avg_width
    avg = leftover/gaps
    return avg

mortar = avg_mortar(heads, head_assembly)


def build_header(ordered_head_list=None, assembly_length=None):
    #cut down list, keep one more than half
    count = ordered_head_list
    keep_num = (count//2) + 1
    keepers = ordered_head_list[0:keep_num]
    
    #identify keystone
    key = keepers[-1]
    
    
    #start adding points
    origin = Rhino.Geometry.Point3d.Origin
    
    
build_header()
