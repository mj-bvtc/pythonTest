import uuid
import rhinoscriptsyntax as rs
import Rhino


class Count:
    """Utility to record block quantities"""
    def __init__(self, color=None):
        self.point = rs.GetPoint()
        self.radius = .2
        self.color = color
        self.block = Block()
        self.circle = None
        self.id = uuid.uuid4()
        self.hatch = None
        self.group_name = None
        self.center = None
        self.group_list = []
        self.add_count()
        self.set_color(color)
        rs.Redraw()


    def add_count(self):
        self.circle = rs.AddCircle(self.point, self.radius)
        self.group_list.append(self.circle)
        self.hatch = rs.AddHatch(self.circle, hatch_pattern="SOLID")
        self.group_list.append(self.hatch)
        self.group_name = rs.AddGroup(group_name=self.id)        
        objs = [self.circle, self.hatch ]
        rs.AddObjectsToGroup(objs, self.id)
        self.check_center()

    def check_center(self):
        self.center = rs.CircleCenterPoint(self.circle)
        print "The count is centered {}".format(self.center)
    
    def get_color(self):
        color = rs.GetColor()
        rs.ObjectColor(self.group_list, color)
    
    def set_color(self, color):
        rs.ObjectColor(self.group_list, color)


class Block:
    """A data representation of a block in the field"""
    def __init__(self):
        self.guid = uuid.uuid4()
        self.id = None
        self.location = None
        self.Type = None
        self.style_number = None
        self.length_number = None
        self.quantity = None
        self.file = r"C:\Users\mkreidler\Desktop\block_test.txt"
        self.read_block()
    
    def write_block(self):
        file = open(self.file, "w")
        for k,v in self.__dict__.iteritems():
            file.write("{},{}\n".format(k,v))
        file.close()
    
    def read_block(self):
        file = open(self.file, "r")
        for line in file:
            k,v = line.split(",")
            if getattr(self, k) is None:
                setattr(self, k, v.replace("\n",""))


def main():

    color = rs.GetColor()
    objs = [Count(color) for i in range(3)]
    for obj in objs:
        print obj.id
    d = Block()
    
    print d.__dict__
    




if __name__ == main():
    main()