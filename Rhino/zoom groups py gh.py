import rhinoscriptsyntax as rs
import time
import scriptcontext as sc
import Rhino




sc.doc = Rhino.RhinoDoc.ActiveDoc

group_lists_copy = []

for g in group_lists:
    g = [str(id).strip().lower() for id in g]
    group_lists_copy.append(g)

sorted_guid2 = [str(i).strip().lower().replace("'","") for i in sorted_guid]


if run==True:

    for i in sorted_guid2:
        for g in group_lists_copy:
            if i in g:
                #print g
                factor = 50
                box = rs.BoundingBox(g)
                box = Rhino.Geometry.BoundingBox(box)
                box.Inflate(factor,factor,factor)
                box = box.GetCorners()
                rs.ZoomBoundingBox(box, view="Front")
                
                time.sleep(delay)
                for guid in g:
                    sorted_guid2.remove(guid)

print "complete"



sc.doc = ghdoc