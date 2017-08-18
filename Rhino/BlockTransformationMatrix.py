import Rhino
import rhinoscriptsyntax as rs



name = raw_input("Type in the name of your block")
blocks = rs.BlockInstances(name)


def test_transformed(guid):
    """
    Tests if a transformation has occured
    in an object
    """
    result = None
    
    xform = rs.BlockInstanceXform(guid)
    
    matrix = [
     xform.M00,
     xform.M01,
     xform.M02,
     #xform.M03, #These values denote translation, not scaling
    
     xform.M10,
     xform.M11,
     xform.M12,
     #xform.M13,
    
     xform.M20,
     xform.M21,
     xform.M22,
     #xform.M23,
    
     xform.M30,
     xform.M31,
     xform.M32,
     #xform.M33
    ]

    #print matrix

    for x in matrix:
        if x == 0:
            continue
        if x == 1:
            continue
        else:
            print x
            return True
    if result == None:
        return False

#print test_transformed(guid)

transformed = [x for x in blocks if test_transformed(x)]

rs.SelectObjects(transformed)

#print transformed