import rhinoscriptsyntax as rs
import os
import getpass
import Rhino
import shutil
import datetime


class Synch:
    ####################################################
    ### Synchronize a workstation to Rhino Standards ###
    ###            Written By: Peter Schmidt         ###
    ###         For: Boston Valley Terra Cotta       ###
    ####################################################
    
    def __init__(self):
        self.Files=[]
        self.Folders=[]
        
        self.templateFolder=rs.TemplateFolder()
        self.syncFile="V:\MeshLab\_Synchronization"
        self.syncLib="V:\MeshLab\_Synchronization\Python_Libraries"
        
        ExFolder=rs.ExeFolder()
        Ex=ExFolder.rstrip("\\System\\")
        self.SysLib=Ex+"\\Plug-ins\\IronPython\\Lib"
        
        self.localFolder=""
        
    def SetTemplate(self,_showMessages=False):
        user=getpass.getuser()
        ## create folder to store local data ##
        folder="C:\\Users\\"+user+"\\AppData\\Local\\BVTC\\"
        if not os.path.isdir(folder):
            try:
                os.makedirs(folder)
            except WindowsError:
                rs.MessageBox("Could not create '"+folder+"' folder.",0,"WindowsError")
                
        if os.path.isdir(folder):
            self.localFolder=folder
        else:
            msg+="Could not create folder."
            return
        
        ## Close Old Toolbars ##
        CurrentTBs=rs.ToolbarCollectionNames()
        for bar in CurrentTBs:
            rs.CloseToolbarCollection(bar,False)
        
        
        files=os.listdir(self.syncFile)
        msg=""
        
        for file in files:
            if not os.path.isdir(file):
                ext=file.split(".")[-1]
                
                ## Copy over 3DM template files ##
                if ext == "3dm":
                    try:
                        shutil.copy(self.syncFile+"\\"+file,self.localFolder+file)
                        msg+="Copied "+file+" to local file."+" \n"
                        
                        ## Update default temple to local copy ##
                        if file=="Synch_Template.3dm":
                            rs.TemplateFile(self.localFolder+file)
                            msg+= self.localFolder+file+" set as default template."+" \n"
                            rs.TemplateFolder(self.localFolder)
                            msg+= self.localFolder+" set as default template folder." +" \n"
                    except:
                        msg+="Could not copy '"+file+"' to '"+self.localFolder+"'"
                
                
                ## Copy over RUI files ##
                if ext.upper() == "RUI":
                    shutil.copy(self.syncFile+"\\"+file,self.localFolder+file)
                    msg+="Copied "+file+" to local file." +" \n"
                    
                    ## Set default Toolbar ##
                    if file.upper()=="SynchToolbar_PlugIn.RUI":
                        msg+="Copied toolbar collection "+file+" to "+self.localFolder+file+" \n"
                        rs.OpenToolbarCollection(self.localFolder+file)
                        msg+="Current toolbar set as "+self.localFolder+file+" \n"
        
        if _showMessages==True:
            print msg
    
    def SetUpDrafting(self):
        CurrentDim=rs.CurrentDimStyle()
        rs.AddHatchPatterns("V:\MeshLab\_Synchronization\Synch_Files\Synch_Hatches.3dm")
        if CurrentDim!="SyncDimSytle":
            print CurrentDim
            print "Set Up Standards"
    
    def SetUpPlugins(self):
        gh = Rhino.RhinoApp.GetPlugInObject("grasshopper")
        if gh:
            print "Grasshopper Installed"
            
        else:
            print "Grasshopper Not Installed"
            Rhino.PlugIns.FileExportPlugIn.IdFromName()
            Rhino.PlugIns.PlugIn.LoadPlugIn()
    
    def SetUpOSnaps(self):
        rs.Osnap(True)
        rs.OsnapDialog(True)
        rs.OsnapMode(134359072)
    
    def RemoveOutdated(self):
        for file in self.Files:
            if os.path.isfile(self.syncLib+"\\"+file)==True:
                if os.path.isfile(self.SysLib+"\\"+file)==True:
                    M_Synch=os.path.getmtime(self.syncLib+"\\"+file)
                    M_Sys=os.path.getmtime(self.SysLib+"\\"+file)
                    if M_Sys<M_Synch:
                        print "--Outdated--"+self.SysLib+"\\"+file+"--Outdated--"
                        try:
                            os.remove(self.SysLib+"\\"+file)
                            print "--Removed--"+self.SysLib+"\\"+file+"--Removed--"
                        except:
                            print "--Failed to Remove--"+self.SysLib+"\\"+file+"--Failed to Remove--"
                        print
        
        for dir in self.Folders:
            if os.path.isdir(self.syncLib+"\\"+dir)==True:
                if os.path.isdir(self.SysLib+"\\"+dir)==True:
                    
                    M_Sys=os.path.getmtime(self.SysLib+"\\"+dir)
                    M_Synch=os.path.getmtime(self.syncLib+"\\"+dir)
                    
                    if M_Sys<M_Synch:
                        print "--Outdated--"+self.SysLib+"\\"+dir+"--Outdated--"
                        try:
                            shutil.rmtree(self.SysLib+"\\"+dir)
                            print "--Removed--"+self.SysLib+"\\"+dir+"--Removed--"
                        except:
                            print "Failed to Remove--"+self.SysLib+"\\"+dir+"Failed to Remove--"
                        print
    
    def IdentifyLibraries(self):
        files=os.listdir(self.syncLib)
        for file in files:
            if file.count(".py")==1:
                self.Files.append(file)
            elif file.count(".")==0:
                self.Folders.append(file)
    
    def AddLibraries(self):
        SynchLib=self.syncFile+"\Python_Libraries"
        
        for file in self.Files:
            ### Add files that are currently missing ###
            if os.path.isfile(self.SysLib+"\\"+file)==False:
                shutil.copy(SynchLib+"\\"+file,self.SysLib+"\\"+file)
                print "Added: "+file+" to Python Libraries"
        
        ###Directories to Synch###
        for dir in self.Folders:
            if os.path.isdir(self.SysLib+"\\"+dir)==False:
                try:
                    shutil.copytree(SynchLib+"\\"+dir,self.SysLib+"\\"+dir)
                    print "Added: "+dir+" to Python Libraries"
                except:
                    print "Failed to Add: "+SynchLib+"\\"+dir

def Synchronize():
    
    sync=Synch()
    """
    try:
        sync.IdentifyLibraries()
        sync.RemoveOutdated()
        sync.AddLibraries()
    except:
        print "you are not an admin."
    """
    sync.SetTemplate(True)
    sync.SetUpOSnaps()
    sync.SetUpDrafting()
    
    
    

Synchronize()
