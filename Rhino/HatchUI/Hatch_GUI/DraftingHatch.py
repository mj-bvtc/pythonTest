import os
import shutil
import rhinoscriptsyntax as rs
import System.Windows.Forms
import System.Drawing
import Meier_UI_Utility
import Rhino
import scriptcontext
from System.Windows.Forms import RadioButton





class HatchUI:
    """The user interface to select hatch and rotation"""

    def __init__(self, txt_path):

        # Make a new form
        self.form = Meier_UI_Utility.UIForm("Hatch Options")
        self.patterns = []
        self.txt_path = txt_path
        self.hatch_list = []
        self.selected_hatch = None
        self.load_hatches()
        self.add_controls()

    def add_controls(self):
        for hatch in self.hatch_list:
            self.add_control(hatch.number)

    def add_control(self, number):
        panel = self.form.panel
        hatch = self.hatch_list[number]
        panel.addPictureBox()
        panel.addPictureBox("hatch_{}".format(hatch.number), hatch.image_path, False)
        panel.addRadioButton("button_{}".format(hatch.number), hatch.description, False, False, self.checked_change)
        panel.addIndent(16)

    def checked_change(self):
        pass

    def load_hatches(self):
        # read text file for hatches/attributes
        f = open(self.txt_path, "r")
        lines = [ln for ln in f]
        hatches = []
        for line in lines:
            entries = [x.strip() for x in line.split(",")]
            hatch = Hatch(int(entries[0]), entries[1], entries[2], float(entries[3]), int(entries[4]), entries[5])
            hatches.append(hatch)
        f.close()
        self.hatch_list = hatches
        return

    def Hatch_Button_Pressed(self, sender, e):
        print "Hatch selected by user"

    def Cancel_Button_Pressed(self, sender, e):
        print "UI cancelled by user"


class Hatch:
    """Hatch object and all its attributes"""

    def __init__(self, number, name, description, scale, rotation, image_path):
        self.number = number
        self.description = description
        self.name = name
        self.scale = scale
        self.rotation = rotation
        self.image_path = image_path


class HatchObjects:
    """The objects to be hatched"""

    def __init__(self):
        self.objects = []
        self.closed_curves = []
        self.open_curves = []
        self.messagebox = None
        self.hatch_pattern = None
        self.hatch_scale = 1.0
        self.hatch_rotation = 0.0
        self.is_hatched = None

    def get_objects(self):
        curves = rs.GetObjects("Select curves to hatch: ", rs.filter.curve)
        num_objs = len(curves)
        if curves is not None:
            print "Selected {} objects".format(num_objs)
            self.objects = curves
        else:
            print "My dude, you did not select anything..."
        return curves

    def check_is_closed(self, crv):
        closed = None
        if rs.IsCurveClosed(crv) is True:
            # print "This curve is AOK"
            closed = True
        else:
            # print "THIS CURVE IS GARBAGE, (and not closed)"
            closed = False
        return closed

    def check_obj_list(self):
        self.closed_curves = [c for c in self.objects if self.check_is_closed(c)]
        self.open_curves = [o for o in self.objects if o not in self.closed_curves]
        print ("There are {} open curves in your selection, they will be skipped".format(len(self.open_curves)))
        return

    def add_hatch(self, curve):
        rs.AddHatch(curve, self.hatch_pattern, self.hatch_scale, self.hatch_rotation)


def main():
    h = HatchObjects()
    h.get_objects()
    h.check_obj_list()
    ui = HatchUI("C:\Users\mkreidler\Desktop\hatches.txt")

    Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    print ui.patterns


if __name__ == "__main__":
    main()