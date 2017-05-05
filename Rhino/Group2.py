import uuid
import rhinoscriptsyntax as rs
import Rhino
import os

doc = Rhino.RhinoDoc.ActiveDoc

root = r"C:\Users\mkreidler\Desktop\project"


# This is a decorator, us @redraw_fast syntax
def redraw_fast(fn):
    def wrapper(*args, **kwargs):
        rs.EnableRedraw(False)
        #print "entering"
        result = fn(*args, **kwargs)
        rs.EnableRedraw(True)
        #print "exiting"
        return result
    return wrapper


class Project:
    def __init__(self):
        self.project = r"C:\Users\mkreidler\Desktop\project"
        self.part = r"C:\Users\mkreidler\Desktop\project\part"
        self.group = r"C:\Users\mkreidler\Desktop\project\group"
        self.material = r"C:\Users\mkreidler\Desktop\project\material"
        self.assembly = r"C:\Users\mkreidler\Desktop\project\assembly"
    
    def add(self, attribute, name):
        path = getattr(self, attribute)
        ids = rs.GetObjects("Select objects to add to group")
        ext = ".txt"
        c = ","
        id_string = c.join([str(id) for id in ids])
        full_path = os.path.join(path,name+ext)
        file = open(full_path, "w")
        file.write(id_string)
        file.close()
        
    #@redraw_fast
    def select(self, input_file):
        file = open(input_file, "r")
        csv = [x for x in file][0]
        ids = csv.split(",")
        rs.SelectObjects(ids)
    
    def select_name(self, attribute, name):
        path = getattr(self, attribute)
        ext = ".txt"
        c = ","
        full_path = os.path.join(path,name+ext)
        self.select(full_path)

@redraw_fast
def main():
    shelf = Project()
    #shelf.add("part", "AllParts")
    #shelf.select(r"C:\Users\mkreidler\Desktop\project\part\AllParts.txt")
    #shelf.add("assembly", "B")
    #shelf.select(r"C:\Users\mkreidler\Desktop\project\assembly\B.txt")
    #shelf.select(r"C:\Users\mkreidler\Desktop\project\assembly\A.txt")
    #shelf.add("assembly", "H")
    #shelf.select_name("material", "Plywood")
    shelf.select_name("assembly", "G")
    shelf.select_name("group", "Top")
    shelf.select_name("material","Plywood")

if __name__ == "__main__":
    main()