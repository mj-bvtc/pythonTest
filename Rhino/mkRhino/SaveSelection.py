"""
Saves a selection out to a text file
"""

import rhinoscriptsyntax as rs
import Rhino
big = r"C:\Users\mkreidler\Desktop\Dump\guids.txt"
small = r"C:\Users\mkreidler\Desktop\Dump\guids2.txt"
huge = r"C:\Users\mkreidler\Desktop\Dump\guids3.txt"

class SaveGuid:
    def __init__(self, path):
        self.path = path
        self.filename = None
        self.root = None
        self.quantity = None
        self.guids = []

    def get_objs(self):
        self.guids =  rs.GetObjects("Select objects to save to file")

    def write(self):
        file = open(self.path, "w")
        for id in self.guids:
            file.write("{}\n".format(id))
        file.close()

    def read(self):
        file = open(self.path, "r")
        for line in file:
            line = line.replace("\n","")
            self.guids.append(line)

    def select_all(self):
        rs.EnableRedraw(False)
        rs.SelectObjects(self.guids)
        rs.EnableRedraw(True)



def main():
    s = SaveGuid(small)
    #s.get_objs()
    #s.write()
    s.read()
    s.select_all()

if __name__ == "__main__":
    main()
