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

    def __init__(self):
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Hatch Options")
        self.patterns = []
        self.add_patterns()
        self.add_controls()

    def add_controls(self):
        panel=self.form.panel
        panel.addPictureBox("hatch0","V:\MeshLab\_Synchronization\Hatch_GUI\mortar_indent.jpg",False)
        panel.addRadioButton("Button0",self.patterns[0],False,False,self.checkedChanged)
        panel.addIndent(16)
        panel.addPictureBox("hatch1","V:\MeshLab\_Synchronization\Hatch_GUI\\treat_for_mortar.jpg",False)
        panel.addRadioButton("Button1",self.patterns[1],False,False,self.checkedChanged)
        panel.addIndent(10)
        panel.addPictureBox("hatch2","V:\MeshLab\_Synchronization\Hatch_GUI\\cells.jpg",False)
        panel.addRadioButton("Button2",self.patterns[2],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch3","V:\MeshLab\_Synchronization\Hatch_GUI\handhold.jpg",False)
        panel.addRadioButton("Button3",self.patterns[3],False,False,self.checkedChanged)
        panel.addIndent(20)
        panel.addPictureBox("hatch4","V:\MeshLab\_Synchronization\Hatch_GUI\\typical_chiselface.jpg",False)
        panel.addRadioButton("Button4",self.patterns[4],False,False,self.checkedChanged)
        panel.addIndent(8)
        panel.addPictureBox("hatch5","V:\MeshLab\_Synchronization\Hatch_GUI\\perforation_area.jpg",False)
        panel.addRadioButton("Button5",self.patterns[5],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch6","V:\MeshLab\_Synchronization\Hatch_GUI\\aluminum.jpg",False)
        panel.addRadioButton("Button6",self.patterns[6],False,False,self.checkedChanged)
        panel.addIndent(24)
        panel.addPictureBox("hatch7","V:\MeshLab\_Synchronization\Hatch_GUI\\CMU.jpg",False)
        panel.addRadioButton("Button7",self.patterns[7],False,False,self.checkedChanged)
        panel.addIndent(29)
        panel.addPictureBox("hatch8","V:\MeshLab\_Synchronization\Hatch_GUI\\concrete.jpg",False)
        panel.addRadioButton("Button8",self.patterns[8],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch9","V:\MeshLab\_Synchronization\Hatch_GUI\insulation.jpg",False)
        panel.addRadioButton("Button9",self.patterns[9],False,False,self.checkedChanged)
        panel.addIndent(24)
        panel.addPictureBox("hatch10","V:\MeshLab\_Synchronization\Hatch_GUI\\sheathing.jpg",False)
        panel.addRadioButton("Button10",self.patterns[10],False,False,self.checkedChanged)
        panel.addIndent(21)
        panel.addPictureBox("hatch11","V:\MeshLab\_Synchronization\Hatch_GUI\\steel.jpg",False)
        panel.addRadioButton("Button11",self.patterns[11],False,True,self.checkedChanged)
        
        
        panel.addPictureBox("hatch12","V:\MeshLab\_Synchronization\Hatch_GUI\\terra_cotta.jpg",False)
        panel.addRadioButton("Button12",self.patterns[12],False,False,self.checkedChanged)
        panel.addIndent(20)
        panel.addPictureBox("hatch13","V:\MeshLab\_Synchronization\Hatch_GUI\\back_up_masonry.jpg",False)
        panel.addRadioButton("Button13",self.patterns[13],False,False,self.checkedChanged)
        panel.addIndent(7)
        panel.addPictureBox("hatch14","V:\MeshLab\_Synchronization\Hatch_GUI\\face_brick.jpg",False)
        panel.addRadioButton("Button14",self.patterns[14],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch15","V:\MeshLab\_Synchronization\Hatch_GUI\\mortar_or_grout.jpg",False)
        panel.addRadioButton("Button15",self.patterns[15],False,False,self.checkedChanged)
        panel.addIndent(1)
        panel.addPictureBox("hatch16","V:\MeshLab\_Synchronization\Hatch_GUI\\random_textured_surface.jpg",False)
        panel.addRadioButton("Button16",self.patterns[16],False,False,self.checkedChanged)
        panel.addIndent(7)
        panel.addPictureBox("hatch17","V:\MeshLab\_Synchronization\Hatch_GUI\\textured_surface.jpg",False)
        panel.addRadioButton("Button17",self.patterns[17],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch18","V:\MeshLab\_Synchronization\Hatch_GUI\\wood_face_surface.jpg",False)
        panel.addRadioButton("Button18",self.patterns[18],False,True,self.checkedChanged)
        
        
        panel.addIndent(170)
        panel.addButton("Cancel_Button","Cancel",75,".\Icons\Cancel.png",False,self.Cancel_Button_Pressed)
        panel.addButton("Hatch_Button","OK",75,".\Icons\OK.png",True,self.Hatch_Button_Pressed)

    def add_patterns(self):
        self.patterns = [
                "Mortar_Indent",
                "Treat_For_Mortar",
                "Cells",
                "Hand_Hold",
                "Typical_Chiselface",
                "Perforation_Area",
                "Aluminum",
                "CMU",
                "Concrete",
                "Insulation",
                "Sheathing",
                "Steel",
                "Terra_Cotta",
                "Back_Up_Masonry",
                "Face_Brick",
                "Mortar_or_Grout",
                "Random_Texture_Surface",
                "Textured_Surface",
                "Wood_Face_Texture"]

    def checkedChanged(self, sender, args):
        if not sender.Checked:
            return
        if sender.Text == self.patterns[0]:
            self.hatchPAT='FLEX'
            self.hatchSCALE=.25
            self.hatchROT=45
        if sender.Text == self.patterns[1]:
            self.hatchPAT='ZIGZAG'
            self.hatchSCALE=.916667
            self.hatchROT=45
        if sender.Text == self.patterns[2]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.5
            self.hatchROT=0
        if sender.Text == self.patterns[3]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.3125
            self.hatchROT=0
        if sender.Text == self.patterns[4]:
            self.hatchPAT='LINE'
            self.hatchSCALE=.395833
            self.hatchROT=90
        if sender.Text == self.patterns[5]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=.29155
            self.hatchROT=0
        if sender.Text == self.patterns[6]:
            self.hatchPAT='ANSI34'
            self.hatchSCALE=.125
            self.hatchROT=0
        if sender.Text == self.patterns[7]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.5
            self.hatchROT=0
        if sender.Text == self.patterns[8]:
            self.hatchPAT='AR-CONC'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.patterns[9]:
            self.hatchPAT='NET'
            self.hatchSCALE=.375
            self.hatchROT=0
        if sender.Text == self.patterns[10]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.03125
            self.hatchROT=0
        if sender.Text == self.patterns[11]:
            self.hatchPAT='ANSI32'
            self.hatchSCALE=.125
            self.hatchROT=0
        if sender.Text == self.patterns[12]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.patterns[13]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=1.252
            self.hatchROT=0
        if sender.Text == self.patterns[14]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=.5634
            self.hatchROT=0
        if sender.Text == self.patterns[15]:
            self.hatchPAT='AR-CONC'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.patterns[16]:
            self.hatchPAT='AR-ROOF'
            self.hatchSCALE=.25
            self.hatchROT=0
        if sender.Text == self.patterns[17]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.036458
            self.hatchROT=0
        if sender.Text == self.patterns[18]:
            self.hatchPAT='AR-ROOF'
            self.hatchSCALE=.0625
            self.hatchROT=90

    def Hatch_Button_Pressed(self,sender,e):
        if rs.IsCurveClosed(self.crv)==True:
            ptLST=[]
            pt0=rs.CurveEndPoint(self.crv,0)
            pt1=rs.CurveEndPoint(self.crv,1)
            pt2=rs.CurveEndPoint(self.crv,2)
            pt3=rs.CurveEndPoint(self.crv,3)
            ptLST.append(pt0)
            ptLST.append(pt1)
            ptLST.append(pt2)
            ptLST.append(pt3)
            plane=rs.PlaneFitFromPoints(ptLST)
            if plane!=None:
                rs.EnableRedraw(False)
                self.boundingBox()
            else:
                rs.MessageBox("aww shit you messed up! /n -Andy Pries",0)

    def Cancel_Button_Pressed(self,sender,e):
        print "Cancel Button Pressed"

class Hatch:
    """Hatch object and all its attributes"""
    def __init__(self, number, name, description, scale, rotation, image_path):
        self.number = number
        self.description = description
        self.name = name
        self.scale = scale
        self.rotation = rotation
        self.image_path = image_path

def load_drafting_hatches():
    indent = Hatch(
            number=0, 
            name="FLEX", 
            description="Mortar Indent", 
            scale=.25, 
            rotation=45, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\treat_for_mortar.jpg")

    treat = Hatch(
            number=1, 
            name="ZIGZAG", 
            description="Treat for Mortar", 
            scale=.916667, 
            rotation=45, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\mortar_indent.jpg")

    cells = Hatch(
            number=2, 
            name="ANSI37", 
            description="Cells", 
            scale=.5, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\cells.jpg")

    hand = Hatch(
            number=3, 
            name="ANSI37", 
            description="Cells", 
            scale=.3125, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\handhold.jpg")

    chisel = Hatch(
            number=4, 
            name="LINE", 
            description="Typical Chiselface", 
            scale=.395833, 
            rotation=90, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\typical_chiselface.jpg")

    perf = Hatch(
            number=5, 
            name="ANSI31", 
            description="Perforated Area", 
            scale=.29155, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\perforation_area.jpg")

    aluminum = Hatch(
            number=6, 
            name="ANSI34", 
            description="Aluminum", 
            scale=.125, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\aluminum.jpg")

    cmu = Hatch(
            number=7, 
            name="ANSI37", 
            description="CMU", 
            scale=.5, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\CMU.jpg")

    conc = Hatch(
            number=8, 
            name="AR-CONC", 
            description="Concrete", 
            scale=.01565, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\concrete.jpg")

    insul = Hatch(
            number=9, 
            name="NET", 
            description="Insulation", 
            scale=.375, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\insulation.jpg")

    sheath = Hatch(
            number=10, 
            name="AR-SAND", 
            description="Sheathing", 
            scale=.03125, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\sheathing.jpg")

    steel = Hatch(
            number=11, 
            name="ANSI32", 
            description="Steel", 
            scale=.125, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\steel.jpg")

    tc = Hatch(
            number=12, 
            name="AR-SAND", 
            description="Terra Cotta", 
            scale=.01565, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\terra_cotta.jpg")

    back = Hatch(
            number=13, 
            name="ANSI31", 
            description="Back-up Masonry", 
            scale=1.252, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\back_up_masonry.jpg")

    brick = Hatch(
            number=14, 
            name="ANSI31", 
            description="Face Brick", 
            scale=.5634, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\face_brick.jpg")

    mortar = Hatch(
            number=15, 
            name="AR_CONC", 
            description="Mortar or Grout", 
            scale=.01565, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\mortar_or_grout.jpg")

    rand = Hatch(
            number=16, 
            name="AR-ROOF", 
            description="Random Textured Surface", 
            scale=.25, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\random_textured_surface.jpg")

    text = Hatch(
            number=17, 
            name="AR-SAND", 
            description="Textured Surface", 
            scale=.0625, 
            rotation=0, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\textured_surface.jpg")

    wood = Hatch(
            number=18, 
            name="AR-ROOF", 
            description="Wood Face Texture", 
            scale=.036458, 
            rotation=90, 
            image_path="V:\MeshLab\_Synchronization\Hatch_GUI\\wood_face_surface.jpg")


    all_hatch = [indent, treat, cells, hand, chisel, perf, aluminum, cmu, conc, 
            insul, sheath, steel, tc, back, brick, mortar, rand, text, wood]

    return all_hatch

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
        curves = rs.GetObjects("Select curves to hatch: ",rs.filter.curve)
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
            #print "This curve is AOK"
            closed = True
        else:
            #print "THIS CURVE IS GARBAGE, (and not closed)"
            closed = False
        return closed
        
    def check_obj_list(self):
        self.closed_curves = [c for c in self.objects if self.check_is_closed(c)]
        self.open_curves = [o for o in self.objects if o not in self.closed_curves]
        print ("There are {} open curves in your selection, they will be skipped".format(len(self.open_curves)))
        return 
        
    def add_hatch(self, curve):
        rs.AddHatch(curve, self.hatch_pattern, self.hatch_scale, self.hatch_rotation) 

def hatch_from_txt(txt_path):
    f = open(txt_path, "r")
    lines = [ln for ln in f]
    hatches = []
    for line in lines:
        entries = [x.strip() for x in line.split(",")]
        hatch = Hatch(entries[0], entries[1], entries[2], entries[3],entries[4], entries[5])
        hatches.append(hatch)
    f.close()
    return hatches




def main():

    h = HatchObjects()
    h.get_objects()
    h.check_obj_list()
    ui = HatchUI()

    Rhino.UI.Dialogs.ShowSemiModal(ui.form)



if __name__ == "__main__":
    
    main()