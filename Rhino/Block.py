import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
import datetime
import uuid
import os

doc = Rhino.RhinoDoc.ActiveDoc



class Block:
    quantity = 0
    instances = []

    def __init__(self):
        Block.quantity += 1
        self.data = None
        self.dot = None
        self.id = uuid.uuid4()
        self.last_update = datetime.datetime.now()
        self.instance = None
        self.point = None
        self.deleted = None
        Block.instances.append(self)


    def update(self):
        dot_obj = doc.Objects.Find(self.dot)
        if dot_obj is None:
            print "'{}' instance-{} has been deleted".format(self.data.name, self.instance)
            self.deleted = True
            return
        else:
            print "'{}' instance-{} exists".format(self.data.name, self.instance)
            dot_geo = dot_obj.Geometry
        point = dot_geo.Point
        if point != self.point:
            print "'{}' instance-{} has been moved".format(self.data.name, self.instance)
            self.point = point
        else:
            print "'{}' instance-{} has not moved".format(self.data.name, self.instance)
        text = dot_geo.Text
        if text != self.data.name:          ###need to watch the instance extension here
            print "'{}' instance-{} has been renamed".format(self.data.name, self.instance)
            self.data.name = text
        else:
            print "'{}' instance-{} name is valid".format(self.data.name, self.instance)

    def zoom(self):
        rs.SelectObject(self.dot)
        rs.ZoomSelected()
    
    def zoom_all(self):
        objs = [x.dot for x in Block.instances]
        rs.SelectObjects(objs)
        rs.ZoomSelected()
    
    # instance = 1 equals first object, 2 is second etc.
    def assign_data(self, data):
        self.data = data
        data.update(self.id)
        self.instance = data.instances[data.name].index(self.id) + 1
        
    def get_point(self):
        self.point = rs.GetPoint("Select Point")
    
    def add_dot(self, show_instance=True):
        if self.point is None:
            self.get_point()
        if show_instance is True:
            self.dot = rs.AddTextDot("{} [{}]".format(self.data.name, self.instance), self.point)
        else:
            self.dot = rs.AddTextDot(self.data.name, self.point)

    def add_increment_dot(self, style_number, show_instance = False):
        self.data.style_number = style_number
        if show_instance is True:            
            self.dot = rs.AddTextDot("{}{} [{}]".format(self.data.style, self.data.style_number, self.instance), self.point)
        else:
            self.dot = rs.AddTextDot("{}{}".format(self.data.style, self.data.style_number), self.point)

class Data:
    instances = {}
    def __init__(self):
        self.id = uuid.uuid4()
        self.style = None
        self.style_number = None
        self.project = None
        self.location = None
        self.phase = None
        self.priority = None
        self.old_names = {}
        self.notes = None
        self.orientation = None


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


def add_blocks(quantity, data):
    objs = [Block() for i in range(quantity)]
    for obj in objs:
        obj.get_point()
        obj.assign_data(data)
        obj.add_dot()
    
    
def add_increment_blocks(quantity, data, start):
    objs = [Block() for i in range(quantity)]
    count = start
    for obj in objs:
        obj.get_point()
        obj.assign_data(data)
        obj.add_increment_dot(count)
        count += 1
        
# This is a decorator, us @redraw_fast syntax
def redraw_fast(fn):
    def wrapper(*args, **kwargs):
        rs.EnableRedraw(False)
        print "entering"
        result = fn(*args, **kwargs)
        rs.EnableRedraw(True)
        print "exiting"
        return result
    return wrapper


class Zone:
    
    def __init__(self):
        self.type = None
        self.value = None
        self.brep = None
        self.point_inside = None
        self.id = None
    
    def get_brep(self):
        self.id = rs.GetObject("get brep", rs.filter.extrusion)
        self.brep = rs.coercebrep(self.id)

    def check_point_inside(self, point):
        self.point_inside = self.brep.IsPointInside(point, rs.UnitAbsoluteTolerance(), False)
        return self.point_inside

    def report(self):
        if self.point_inside is True:
            message = "Point is on {} {}".format(self.type, self.value)
        else:
            message = "Point is outside of {} {}".format(self.type, self.value)
        print message

def main():
    d = Data()
    d.style = "RT"
    d.project = "P15-0509"
    d.phase = "Base"

    add_increment_blocks(16, d,8)
    
    for block in Block.instances:
        block.update()

    #os.startfile(r"C:\Users\mkreidler\Desktop\test.csv")
    #print Block.quantity



if __name__ == "__main__":
    main()
