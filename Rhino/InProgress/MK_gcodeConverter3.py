import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
doc = Rhino.RhinoDoc.ActiveDoc

class Gcode():
    """This is a gcode generator class"""
    def __init__(self):
        self.file_contents = None
        self.file_path = self.get_save_file()
        self.file_body = None
        self.start_code = "M91\nG74\nM58\nG90\nM11\n" ##M91 is relative
        self.end_code = "M21\nM02"

    
    def get_save_file(self):
        sd = Rhino.UI.SaveFileDialog()
        Rhino.UI.SaveFileDialog.ShowDialog(sd)
        filename = sd.FileName + ".txt"
        return filename

    
    def add_line(self, code_line):
        if self.file_body:
            self.file_body += (code_line + "\n")
            print "Added line to code"
        else:
            self.file_body = (code_line + "\n")
            print "Added first line to code"
    
    def combine_code(self):
        self.file_contents = self.start_code
        self.file_contents += self.file_body
        self.file_contents += self.end_code


    def save(self):
        self.combine_code()
        file = open(self.file_path, "w")
        file.write(self.file_contents)
        file.close()
        print "Saved file to: " + self.file_path


def gcode_test():
    file = Gcode()
    file.add_line("This is a test, again")
    file.add_line("here is a second line")
    file.save()

def sort_selection(objects):
    for obj in objects:
        rh_obj = doc.Objects.Find(obj)
        sub_objs = rh_obj.GetSubObjects()
        for sub in sub_objs:
            print sub



def main():
    objects = rs.GetObjects("Select curves to turn into Gcode")
    sort_selection(objects)









if __name__ == "__main__":
    main()