import os
import shutil
import rhinoscriptsyntax as rs
import System.Windows.Forms
import System.Drawing
import Meier_UI_Utility
import Rhino
import scriptcontext
from System.Windows.Forms import RadioButton



def Main():
    Current=rs.CurrentLayer()
    crv=rs.GetObject("Select curve to hatch: ",rs.filter.curve)
    
    # Make the UI object
    if crv != None:
        if rs.IsCurveClosed(crv):
            ui = HatchControlWindow(crv)
            # Show the dialog from the UI class
            Rhino.UI.Dialogs.ShowSemiModal(ui.form)
            rs.CurrentLayer(Current)
        else:
            rs.MessageBox("Selected Curve is Not Closed.")

class HatchControlWindow():
    def __init__(self,crv):
        self.crv=crv
        
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Hatch Options") 
        # Accumulate controls for the form
        
        self.hatchPatLST=[]
        self.hatchPatLST.append("Mortar_Indent")
        self.hatchPatLST.append("Treat_For_Mortar")
        self.hatchPatLST.append("Cells")
        self.hatchPatLST.append("Hand_Hold")
        self.hatchPatLST.append("Typical_Chiselface")
        self.hatchPatLST.append("Perforation_Area")
        self.hatchPatLST.append("Aluminum")
        self.hatchPatLST.append("CMU")
        self.hatchPatLST.append("Concrete")
        self.hatchPatLST.append("Insulation")
        self.hatchPatLST.append("Sheathing")
        self.hatchPatLST.append("Steel")
        self.hatchPatLST.append("Terra_Cotta")
        self.hatchPatLST.append("Back_Up_Masonry")
        self.hatchPatLST.append("Face_Brick")
        self.hatchPatLST.append("Mortar_or_Grout")
        self.hatchPatLST.append("Random_Texture_Surface")
        self.hatchPatLST.append("Textured_Surface")
        self.hatchPatLST.append("Wood_Face_Texture")
        
        self.addControls()
        # Layout the controls on the form
        self.form.layoutControls()
    
    def addControls(self):
        panel=self.form.panel
        
        #panel.addPictureBox("Logo",".\Icons\Logo.jpg",True)
        
        panel.addPictureBox("hatch0","V:\MeshLab\_Synchronization\Hatch_GUI\mortar_indent.jpg",False)
        panel.addRadioButton("Button0",self.hatchPatLST[0],False,False,self.checkedChanged)
        panel.addIndent(16)
        panel.addPictureBox("hatch1","V:\MeshLab\_Synchronization\Hatch_GUI\\treat_for_mortar.jpg",False)
        panel.addRadioButton("Button1",self.hatchPatLST[1],False,False,self.checkedChanged)
        panel.addIndent(10)
        panel.addPictureBox("hatch2","V:\MeshLab\_Synchronization\Hatch_GUI\\cells.jpg",False)
        panel.addRadioButton("Button2",self.hatchPatLST[2],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch3","V:\MeshLab\_Synchronization\Hatch_GUI\handhold.jpg",False)
        panel.addRadioButton("Button3",self.hatchPatLST[3],False,False,self.checkedChanged)
        panel.addIndent(20)
        panel.addPictureBox("hatch4","V:\MeshLab\_Synchronization\Hatch_GUI\\typical_chiselface.jpg",False)
        panel.addRadioButton("Button4",self.hatchPatLST[4],False,False,self.checkedChanged)
        panel.addIndent(8)
        panel.addPictureBox("hatch5","V:\MeshLab\_Synchronization\Hatch_GUI\\perforation_area.jpg",False)
        panel.addRadioButton("Button5",self.hatchPatLST[5],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch6","V:\MeshLab\_Synchronization\Hatch_GUI\\aluminum.jpg",False)
        panel.addRadioButton("Button6",self.hatchPatLST[6],False,False,self.checkedChanged)
        panel.addIndent(24)
        panel.addPictureBox("hatch7","V:\MeshLab\_Synchronization\Hatch_GUI\\CMU.jpg",False)
        panel.addRadioButton("Button7",self.hatchPatLST[7],False,False,self.checkedChanged)
        panel.addIndent(29)
        panel.addPictureBox("hatch8","V:\MeshLab\_Synchronization\Hatch_GUI\\concrete.jpg",False)
        panel.addRadioButton("Button8",self.hatchPatLST[8],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch9","V:\MeshLab\_Synchronization\Hatch_GUI\insulation.jpg",False)
        panel.addRadioButton("Button9",self.hatchPatLST[9],False,False,self.checkedChanged)
        panel.addIndent(24)
        panel.addPictureBox("hatch10","V:\MeshLab\_Synchronization\Hatch_GUI\\sheathing.jpg",False)
        panel.addRadioButton("Button10",self.hatchPatLST[10],False,False,self.checkedChanged)
        panel.addIndent(21)
        panel.addPictureBox("hatch11","V:\MeshLab\_Synchronization\Hatch_GUI\\steel.jpg",False)
        panel.addRadioButton("Button11",self.hatchPatLST[11],False,True,self.checkedChanged)
        
        
        panel.addPictureBox("hatch12","V:\MeshLab\_Synchronization\Hatch_GUI\\terra_cotta.jpg",False)
        panel.addRadioButton("Button12",self.hatchPatLST[12],False,False,self.checkedChanged)
        panel.addIndent(20)
        panel.addPictureBox("hatch13","V:\MeshLab\_Synchronization\Hatch_GUI\\back_up_masonry.jpg",False)
        panel.addRadioButton("Button13",self.hatchPatLST[13],False,False,self.checkedChanged)
        panel.addIndent(7)
        panel.addPictureBox("hatch14","V:\MeshLab\_Synchronization\Hatch_GUI\\face_brick.jpg",False)
        panel.addRadioButton("Button14",self.hatchPatLST[14],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch15","V:\MeshLab\_Synchronization\Hatch_GUI\\mortar_or_grout.jpg",False)
        panel.addRadioButton("Button15",self.hatchPatLST[15],False,False,self.checkedChanged)
        panel.addIndent(1)
        panel.addPictureBox("hatch16","V:\MeshLab\_Synchronization\Hatch_GUI\\random_textured_surface.jpg",False)
        panel.addRadioButton("Button16",self.hatchPatLST[16],False,False,self.checkedChanged)
        panel.addIndent(7)
        panel.addPictureBox("hatch17","V:\MeshLab\_Synchronization\Hatch_GUI\\textured_surface.jpg",False)
        panel.addRadioButton("Button17",self.hatchPatLST[17],False,True,self.checkedChanged)
        
        panel.addPictureBox("hatch18","V:\MeshLab\_Synchronization\Hatch_GUI\\wood_face_surface.jpg",False)
        panel.addRadioButton("Button18",self.hatchPatLST[18],False,True,self.checkedChanged)
        
        
        panel.addIndent(170)
        panel.addButton("Cancel_Button","Cancel",75,".\Icons\Cancel.png",False,self.Cancel_Button_Pressed)
        panel.addButton("Hatch_Button","OK",75,".\Icons\OK.png",True,self.Hatch_Button_Pressed)
    
    def checkedChanged(self, sender, args):
        if not sender.Checked:
            return
        if sender.Text == self.hatchPatLST[0]:
            self.hatchPAT='FLEX'
            self.hatchSCALE=.25
            self.hatchROT=45
        if sender.Text == self.hatchPatLST[1]:
            self.hatchPAT='ZIGZAG'
            self.hatchSCALE=.916667
            self.hatchROT=45
        if sender.Text == self.hatchPatLST[2]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.5
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[3]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.3125
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[4]:
            self.hatchPAT='LINE'
            self.hatchSCALE=.395833
            self.hatchROT=90
        if sender.Text == self.hatchPatLST[5]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=.29155
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[6]:
            self.hatchPAT='ANSI34'
            self.hatchSCALE=.125
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[7]:
            self.hatchPAT='ANSI37'
            self.hatchSCALE=.5
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[8]:
            self.hatchPAT='AR-CONC'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[9]:
            self.hatchPAT='NET'
            self.hatchSCALE=.375
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[10]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.03125
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[11]:
            self.hatchPAT='ANSI32'
            self.hatchSCALE=.125
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[12]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[13]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=1.252
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[14]:
            self.hatchPAT='ANSI31'
            self.hatchSCALE=.5634
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[15]:
            self.hatchPAT='AR-CONC'
            self.hatchSCALE=.01565
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[16]:
            self.hatchPAT='AR-ROOF'
            self.hatchSCALE=.25
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[17]:
            self.hatchPAT='AR-SAND'
            self.hatchSCALE=.036458
            self.hatchROT=0
        if sender.Text == self.hatchPatLST[18]:
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
    
    def boundingBox(self):
        lnLST=[]
        bb=rs.BoundingBox(self.crv)
        ln0=rs.AddLine(bb[0],bb[1])
        ln1=rs.AddLine(bb[1],bb[2])
        ln2=rs.AddLine(bb[2],bb[3])
        ln3=rs.AddLine(bb[3],bb[0])
        lnLST.append(ln0)
        lnLST.append(ln1)
        lnLST.append(ln2)
        lnLST.append(ln3)
        self.box=rs.JoinCurves(lnLST,True)
        centroid=rs.CurveAreaCentroid(self.box)
        rs.ScaleObjects(self.box,centroid[0],(1.2,1.2,1.2),False)
        
        self.addHatch()
    
    def addHatch(self):
        #self.hatch=rs.AddHatch(self.box,self.hatchPAT,self.hatchSCALE,self.hatchROT)
        srf=rs.AddPlanarSrf(self.box)
        ext=rs.ExtrudeCurveStraight(self.crv,(0,0,-1),(0,0,1))
        #rs.FlipSurface(srf,True)
        trimSrf=rs.SplitBrep(srf,ext,None)
        rs.DeleteObject(ext)
        rs.DeleteObjects(self.box)
        rs.DeleteObject(srf)
        rs.DeleteObject(trimSrf[0])
        newCrv=rs.DuplicateSurfaceBorder(trimSrf[1],0)
        
        ## Make/Check Layers ##
        if rs.IsLayer("TITLEBLOCK")!=True:
            TitleLayer=rs.AddLayer("TITLEBLOCK")
        if rs.IsLayer("Template")!=True:
            rs.AddLayer("Template",None,True,False,"TITLEBLOCK")
        if rs.IsLayer("Hatch")!=True:
            rs.AddLayer("Hatch",None,True,False,"Template")
        
        rs.CurrentLayer("Hatch")
        self.hatch=rs.AddHatch(newCrv,self.hatchPAT,self.hatchSCALE,self.hatchROT)
        rs.DeleteObjects(trimSrf)
        rs.DeleteObject(newCrv)
        
        rs.EnableRedraw(False)
    
    def Cancel_Button_Pressed(self,sender,e):
        print "Cancel Button Pressed"


Main()