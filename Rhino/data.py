import uuid


class Data:
    def __init__(self):
        self.id = uuid.uuid4()
        print "hello"
    
    def update():
        pass
    
    def match(data):
        pass
    


class Project(Data):
    def __init__(self):
        Data.__init__(self)
        self.name = None
        self.address = None
        self.quantity = None
        self.contact = None
        self.phase = None

class BlockData(Data):
    def __init__(self):
        Data.__init__(self)
        self.name = None
        self.orientation = None
        self.colors = None
        self.old_names = {}
        self.style = None
        self.style_number = None
        self.region = None
        self.ornament = None
        self.size = None
        self.form_method = None
        self.is_sample = None
        self.is_hole = None

class Count(Data):
    def __init__(self):
        Data.__init__(self)
        self.color = None
        self.links = []
        
    def add(self):
        pass
    def delete(self):
        pass
    def get_data(self):
        pass

class Group(Data):
    def __init__(self):
        Data.__init__(self)
        self.items = []
    
    @property
    def count(self):
        return len(self.items)
    
    def add(self, *items):
        for item in items:
            if item not in self.items:
                self.items.append(item)
    
    def remove(self, *items):
        for item in items:
            if item in self.items:
                self.items.remove(item)
    
    def split(self, objs):
        a = Group()
        b = Group()

d = Project()
print d.id