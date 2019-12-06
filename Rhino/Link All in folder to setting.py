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


folder = r"C:\Users\mkreidler\Desktop\Test hyperlinks"

dots = rs.GetObjects()




#os.startfile(r"C:\Users\mkreidler\Desktop\test.jpeg")


def attach_hyperlink_2():
    rc, obj_ref = RhinoGet.GetOneObject("Select object", False, ObjectType.AnyObject)
    if rc != Result.Success:
        return rc
    rhino_object = obj_ref.Object()
    file = rs.OpenFileName()
    fmt = format_url(file)
    print fmt
    rhino_object.Attributes.Url = fmt
    rhino_object.CommitChanges()

def format_url(file):
    prefix = r"file:///"
    file_no_space = file.replace(" ", r"%20")
    result = "{}{}".format(prefix, file_no_space)
    return result



attach_hyperlink_2()