import rhinoscriptsyntax as rs
import Rhino
import os



def FindOBJs():
    count=0
    ## Find folder for Agi Renders ##
    
    agiFolder= r"V:\Projects\PS 104K\_Field Work Folder PS104K\Agi-Renders"
    if not agiFolder: return
    
    ## Loop through files ##
    tree=os.walk(agiFolder)
    for dirpath, dirnames, filenames in tree:
        for file in filenames:
            ext=file.split(".")[-1]
            if ext.upper() == "OBJ":
                if check_for_3dm(dirpath)==False:
                    AgiImport(dirpath,file)
                    print "Created File: "+dirpath+file
                    print dirpath + file
                    count+=1
    print "Created "+str(count)+" Rhino files."

def check_for_3dm(folder):
    """
    Check to if a Rhino .3dm file
    exists in a folder.
    """
    find=False;
    if not os.path.exists(folder): return;
    
    walk=os.walk(folder);
    for dirpath, dirnames, filenames in walk:
        for file in filenames:
            ext=file.split(".")[-1];
            if ext.upper()=="3DM":
                find = True;
                return find;
    
    return find

def AgiImport(dirpath, file):
    """
    Create new rhino file, import mesh, split, then save.
    """
    objPath=dirpath+'\\'+file
    if os.path.exists(objPath)==False:
        print objPath
        return
    
    ## Open new template file ##
    template = rs.TemplateFile()
    cmd="-_New "
    cmd+=template+" "
    rs.Command(cmd)
    
    
    cmd="-_Import "
    cmd+='"'+os.path.abspath(objPath)+'"'+" "
    cmd+="IgnoreTextures=No "
    cmd+="MapOBJToRhinoZ=Yes "
    cmd+="_Enter "
    rs.Command(cmd)
    
    rs.Command("SplitDisjointMesh ")
    
    meshes = rs.LastCreatedObjects()
    max=0
    keep=None
    for guid in meshes:
        mesh = rs.coercemesh(guid)
        count = mesh.Faces.Count
        if count > max:
            keep = guid
            max = count
    
    if keep:
        meshes.remove(keep)
    rs.DeleteObjects(meshes)
    
    rs.ZoomExtents(all=True)
    
    cmd="-_SaveAs "
    cmd+="SaveTextures=Yes "
    cmd+='"'+os.path.abspath(objPath).replace(".obj",".3dm")+'"'+" "
    cmd+="_Enter "
    rs.Command(cmd)
    rs.DocumentModified(False)
    Rhino.RhinoApp.Wait()

if __name__=="__main__":
    
    
    FindOBJs()
    #AgiImport(dirpath,file)