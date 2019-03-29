import rhinoscriptsyntax as rs



#get object
ids = rs.GetObjects("Select objects to move")

#make box
box = rs.BoundingBox(ids)
corner = box[0]
translation = corner * -1

#move object to origin
rs.MoveObjects(ids, translation)

#message success
print "Objects moved successfully to origin!"