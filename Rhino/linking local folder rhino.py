import rhinoscriptsyntax as rs
import Rhino
import os
from System.Drawing import *
from Rhino import *
from Rhino.DocObjects import *
from Rhino.Geometry import *
from Rhino.Input import *
from Rhino.Commands import *
from Rhino.UI.Dialogs import ShowColorDialog
from scriptcontext import doc


#os.startfile(r"C:\Users\mkreidler\Desktop\test.jpeg")

def get_link_from_user():
    obj = rs.GetObject()
    
    link = rs.GetUserText(obj, key="link")
    
    print link
    
    os.startfile(link)

def attach_hyperlink_2():
    #rc, obj_ref = RhinoGet.GetOneObject("Select object", False, ObjectType.AnyObject)
    #print obj_ref
    #if rc != Result.Success:
        #return rc
    #rhino_object = obj_ref.Object()
    #points = rs.GetPoints()
    #leader = rs.AddLeader(points, text= raw_input())
    
    rs.Command("!_Leader ")
    leader = rs.LastCreatedObjects()[0]

    rhino_object = Rhino.RhinoDoc.ActiveDoc.Objects.Find(leader)
    
    #file = rs.OpenFileName()
    file = rs.BrowseForFolder()
    fmt = format_url(file)
    print fmt
    rhino_object.Attributes.Url = fmt
    rhino_object.CommitChanges()

def format_url(file):
    prefix = r"file:///"
    a = file.replace("%","%25")
    b = a.replace("#", r"%23")
    c = b.replace(" ", "%20")
    d = c.replace("^","%5E")
    e = d.replace("{","%7B")
    f = e.replace("}","%7D")
    g = f#f.replace("~","%7E")
    h = g#g.replace("[","%5B")
    i = h#h.replace("]","%5D")
    j = i.replace("`","%60")
    k = j.replace(";","%3B")
    l = k#k.replace("=","3D")

    
    result = "{}{}".format(prefix, l)
    return result



attach_hyperlink_2()

