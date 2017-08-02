import Rhino 
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs



def write_file(filename, text=None, filter=None, objects=None):
    print "Saving file as '{}.txt'...\n".format(filename)
    
    print "M90"
    print "G74"
    print "M58"
    print "G91"
    print "M11"
    
    #convert to gcode here
    print "\ninsert gcode here\n"
    #join curves
    #get objects
    #show direction _dir
    #unselectallobjects
    #redraw
    #objectsToCode function
    
    print "M21"
    print "M02"

write_file("Gerbil")


def line_to_code():
    pass

def arc_to_code():
    pass

def polyline_to_code():
    pass

def polycurve_to_code():
    pass

def rounding(num):
    return round(num, 4)


print rounding(5.123456789)
