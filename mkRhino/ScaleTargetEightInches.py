import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino


#get mesh
mesh_id = rs.GetObject("Select Mesh")

#turn off osnaps
rs.Osnap(False)

#get points between 8" targets
start = rs.GetPoint("Click center of target 1")
end = rs.GetPoint("Click center of target 3, 8 inches away")

#calculate scale factor
distance = rs.Distance(start, end)
actual = 8                       ###change this to 4 if necessary
factor = 1/(distance/actual)
scale = [factor, factor, factor]
#scale object from points
new_id = rs.ScaleObject(mesh_id, start, scale)

print "Distance between objects is {0} inches".format(actual)