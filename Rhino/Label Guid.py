import rhinoscriptsyntax as rs
import uuid
import getpass
import socket
import datetime
import json

guids = []
names = []
types = []


class Common(object):
    def __init__(self):
        self.guid = uuid.uuid4()
        self.created_datetime = datetime.datetime.now()
        self.user_name = getpass.getuser()
        self.user_computer = socket.gethostname()

class Collection(Common):
    def __init__(self):
        super(Collection, self).__init__()
        self.guids = []
        self.names = []
        self.types = []

class Zone(Common):
    def __init__(self, collection):
        super(Zone, self).__init__()
        self.type = None
        self.name = None
        self.guid = None
        self.collection = collection
        self.dot = None
        self.point = None
    
    def label(self):
        self.guid = rs.GetObject("Select Zone")
        self.type = raw_input("Input Type")
        self.name = raw_input("Input Label")
        self.collection.types.append(self.type)
        self.collection.names.append(self.name)
        self.collection.guids.append(self.guid)
        self.point = rs.GetPoint("Choose where to label")
        text = "[{}-{}]  {}".format(self.type, self.name, self.guid)
        self.dot = rs.AddTextDot(text, self.point)
        print text
        return text
    
    def labels(self, num=1):
        for i in range(num):
            self.label()


def main():
    c = Collection()
    z = Zone(c)
    z.labels(3)

if __name__ == "__main__":
    main()


