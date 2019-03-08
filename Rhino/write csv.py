import uuid
import rhinoscriptsyntax as rs
import uuid
import getpass
import socket
import datetime
import json



class Common(object):
    def __init__(self):
        self.guid = uuid.uuid4()
        self.created_datetime = datetime.datetime.now()
        self.user_name = getpass.getuser()
        self.user_computer = socket.gethostname()

class Collection(Common):
    def __init__(self):
        super(Collection, self).__init__()
        self.guids = ["GUID"]
        self.names = ["Name"]
        self.types = ["Type"]

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
            
    def write_csv(self, path):
        with open(path, 'w') as f:
            for i in range(len(self.collection.types)):
                t = self.collection.types[i]
                n = self.collection.names[i]
                g = self.collection.guids[i]
                f.write("{},{},{}\n".format(t, n, g))
                



def main():
    path = r"C:\Users\mkreidler\Desktop\test2.csv"
    c = Collection()
    z = Zone(c)
    z.labels(3)
    z.write_csv(path)

if __name__ == "__main__":
    main()
