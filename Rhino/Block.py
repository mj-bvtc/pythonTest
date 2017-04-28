import rhinoscriptsyntax as rs
import Rhino
import datetime
import uuid

class Block:
    
    quantity = 0
    dots = []
    datas = []
    def __init__(self):
        Block.quantity += 1
        self.data = None
        self.dot = None
        self.id = uuid.uuid4()
        self.last_update = datetime.datetime.now()
        self.instance = None

    def zoom(self):
        print "zoom in construction"
    
    def zoom_all(self):
        print "zoom all in construction"
    
    def assign_data(self, data):
        self.data = data
        data.update(self.id)
        self.instance = data.instances[data.name].index(self.id) + 1



class Data:
    instances = {}
    def __init__(self):
        self.style = None
        self.style_number = None
        self.project = None
        self.location = None
        self.phase = None
        self.priority = None
        self.old_names = {}
        self.notes = None


    @property
    def name(self):
        return self.style + str(self.style_number)
    
    def update(self, id):
        if self.name not in Data.instances:
            Data.instances[self.name] = [id]

        else:
            Data.instances[self.name].append(id)




class Location:
    
    def __init__(self):
        self.xyz = None
        self.floor = None
        self.wall = None
        self.section = None



a = Block()
b = Block()

d = Data()
d.style = "BK"
d.style_number = 4
d.project = "P15-0509"
d.phase = "Base"


a.assign_data(d)
b.assign_data(d)
print a.data.instances
print a.instance
print b.instance


