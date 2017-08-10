import uuid
import LogStamp
from status import Status
from common import Common


class Count(Common):

    def __init__(self, *data):
        super(Count, self).__init__()
        self.items = []
        self.add(*data)
    def add(self, *item):
        for i in item:
            self.items.append(i)
    def describe(self):
        for i in self.items:
            print "{}: '{}'".format(i.__class__.__name__, i.name)

class Project(Common):
    def __init__(self):
        super(Project, self).__init__()
        self.name = None
        self.number = None
        self.status = None


class Zone(Common):
    def __init__(self, name):
        super(Zone, self).__init__()
        self.name = name

def main():
    z = Zone("Floor 1")
    zz = Zone("East wing")
    p = Project()
    c = Count(z, p, zz)
    
    p.name = "Woolworth"
    p.number = 123
    p.status = Status.active
    
    c.describe()


if __name__ == "__main__":
    main()