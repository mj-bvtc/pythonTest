import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
doc = Rhino.RhinoDoc.ActiveDoc

#outline boundingbox
def outline():
    rs.Command("_BoundingBox _pause _enter ")
    box = rs.LastCreatedObjects(select=True)
    rs.Command("_Silhouette enter")
    

def outline_box(box):
    rs.SelectObject(box)
    rs.Command("_Silhouette enter")
    rs.DeleteObject(box)

def box_from_dims(w, l, h):
    cmd = "_Box "
    cmd += "0,0,0 "
    cmd += (str(w) + " " )
    cmd += (str(l) + " "  )
    cmd += (str(h) + " "  )
    rs.Command(cmd)
    box = rs.LastCreatedObjects()
    return box

def main():
    width = raw_input("Enter width ")
    length = raw_input("Enter length ")
    height = raw_input("Enter height ")
    box = box_from_dims(width,length,height)
    outline_box(box)
    



if __name__ == "__main__":
    main()