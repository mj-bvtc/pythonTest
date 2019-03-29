ZEimport uuid
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
        #self.guids = ["GUID"]
        #self.names = ["Name"]
        #self.types = ["Type"]
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
        text = "{}-{}".format(self.type, self.name)
        self.dot = rs.AddTextDot(text, self.point)
        print text
        return text
        
    def label_same_type(self):
        num = int(raw_input("Number of zones to label"))
        self.type = raw_input("Input Type for all zones ")
        
        for i in range(num):
            self.guid = rs.GetObject("Select Zone")
            self.name = raw_input("Input Label")
            self.collection.types.append(self.type)
            self.collection.names.append(self.name)
            self.collection.guids.append(self.guid)
            self.point = rs.GetPoint("Choose where to label")
            text = "{}-{}".format(self.type, self.name)
            self.dot = rs.AddTextDot(text, self.point)
            print text
            
            
    def label_areas(self):
        
        areas = rs.GetObjects("Select Zones/Areas")
        self.type = "Area"
        
        for i, a in enumerate(areas):
            result = rs.CurveAreaCentroid(a)
            point = result[0]
            error = result[1]
            self.guid = a
            self.name = i
            self.collection.types.append(self.type)
            self.collection.names.append(self.name)
            self.collection.guids.append(self.guid)
            self.point = point
            text = "{}-{}".format(self.type, self.name)
            self.dot = rs.AddTextDot(text, self.point)
            print text
            

    def label_blocks(self):
        
        areas = rs.GetObjects("Select Zones/Areas")
        self.type = "Block"
        
        for i, a in enumerate(areas):
            result = rs.PointCoordinates(a)
            point = result
            self.guid = a
            self.name = i
            self.collection.types.append(self.type)
            self.collection.names.append(self.name)
            self.collection.guids.append(self.guid)
            self.point = point
            text = "{}-{}".format(self.type, self.name)
            self.dot = rs.AddTextDot(text, self.point)
            print text
            


    
    def labels(self, num=1):
        for i in range(num):
            self.label()
            
    def write_csv(self, path):
        with open(path, 'a') as f:
            for i in range(len(self.collection.types)):
                t = self.collection.types[i]
                n = self.collection.names[i]
                g = self.collection.guids[i]
                f.write("{},{},{}\n".format(t, n, g))
                



def main():
    path = r"C:\Users\mkreidler\Desktop\test.csv"
    c = Collection()
    z = Zone(c)
    z.label_blocks()
    z.write_csv(path)

if __name__ == "__main__":
    main()
