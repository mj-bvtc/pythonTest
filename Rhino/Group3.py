import rhinoscriptsyntax as rs
import Rhino
import os


class Group:
    
    def __init__(self):
        self.root = None
        self.groups = []

    def add_root(self, path):
        self.root = path
        
    def add_group(self, *names):
        for name in names:
            self.groups.append(name)

    def write_to_file(self, filename):
        path = os.path.join(self.root, filename + ".txt")
        if os.path.exists(path) is True:
            file = open(path, "a")
        else:
            file = open(path, "w")
        
        cr = "\n"
        group_string = cr.join(self.groups)
        file.write(group_string)
        file.write("\n")
        file.close()
    
    def format_path(self, filename):
        path = os.path.join(self.root, filename + ".txt")
        return path
    
    
    def read_file(self, filename):
        path = os.path.join(self.root, filename + ".txt")
        if os.path.exists(path) is True:
            file = open(path, "r")
            file.close()
        else:
            print "file not found"
            
    def add_to_file(self, filename, *groups):
        self.add_group(*groups)
        self.write_to_file(filename)
        self.read_file(filename)
        
    def add_guids(self, filename):
        stuff = tuple([str(x) for x in rs.GetObjects("Get Stuff")])
        self.add_to_file(filename, *stuff)
    
    def print_log(self, filename):
        filename = self.format_path(filename)
        file = open(filename, "r")
        for line in file:
            print line.strip()
        file.close()


def main():
    a = Group()
    a.add_root(r"C:\Users\mkreidler\Desktop\church")    
    a.add_guids("points")
    a.print_log("points")


if __name__ == "__main__":
    main()