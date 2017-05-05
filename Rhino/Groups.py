import uuid
import rhinoscriptsyntax as rs
import Rhino

doc = Rhino.RhinoDoc.ActiveDoc


class Group:
    
    def __init__(self, name=None):
        self.name = name
        self.ids = []
        self.file = None
    
    @property
    def count(self):
        if self.ids is not None:
            return len(self.ids)
        else: 
            return None
    
    def add_ids(self):
        self.ids = rs.GetObjects("Select objects to add to group")

    def save_file(self, path):
        file = open(path, 'w')
        self.file = file
        file.write(self.name + ",")
        c = ","
        id_string = c.join(self.ids)
        file.write(id_string)
        file.close()

    def read_file(self, readFile):
        file = open(readFile, "r")
        csv = [x for x in file][0]
        self.name = csv.split(",")[0]
        self.ids = csv.split(",")[1:]
    
    def sel_ids(self):
        rs.SelectObjects(self.ids)

#a = Group("Assembly A")
#a.add_ids()
#a.save_file(r"C:\Users\mkreidler\Desktop\GroupA.txt")
rs.EnableRedraw(False)
b = Group()
b.read_file(r"C:\Users\mkreidler\Desktop\GroupA.txt")
b.sel_ids()
rs.EnableRedraw(True)
print b.ids
print b.name
print b.count
