import rhinoscriptsyntax as rs
import Rhino
import os



def FindOBJs():
    count=0
    ## Find folder for Agi Renders ##
    

    agiFolder= r"F:\222 Central Park South\_Dump\_unprocessed"

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

def AgiImport(objPath):
    """
    Create new rhino file, import mesh, split, then save.
    """
    objPath
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
    cmd+='"'+os.path.abspath(objPath).replace(".wrl",".3dm")+'"'+" "
    cmd+="_Enter "
    rs.Command(cmd)
    rs.DocumentModified(False)
    Rhino.RhinoApp.Wait()
    Rhino.RhinoApp.Wait()

def find_files(path):
    #objs = []
    #rhinos = []
    #wrls = []
    
    walk = os.walk(path)
    
    for dirpath, dirname, filename in walk:
        for file in filename:
            ext = file.split(".")[-1]
            if ext.upper() == "OBJ":
                print "OBJ found: " + file
                objs.append(file)
                full_objs.append(dirpath+'\\'+file)
                
            if ext.upper() == "3DM":
                print "Rhino found: " + file
                rhinos.append(file)
                full_rhinos.append(dirpath+'\\'+file)
            
            if ext.upper() == "WRL":
                print "WRL found: " + file
                wrls.append(file)
                full_wrls.append(dirpath+'\\'+file)
    
    obj_count = len(objs)
    rhino_count = len(rhinos)
    wrl_count = len(wrls)
    
    report = "There were {} OBJ files, {} Rhino files, and {} WRL files found here: {}".format(obj_count, rhino_count, wrl_count, path)
    print ""
    print report

def compare_lists(objs, wrls, rhinos):
    process = []
    process.extend(objs)
    process.extend(wrls)
    
    for file in process:
        base = file.split( ".")[0]
        print base
        rh = base + ".3dm"
        if rh in rhinos:
            process.remove(file)
    return process





if __name__=="__main__":
    
    #path to search
    path = r"V:\Sample Data\Allendale Theater"
    
    #create empy lists to populate
    objs = []
    rhinos = []
    wrls = []
    full_objs = []
    full_wrls = []
    full_rhinos = []

    #search through path and populate lists if objs, wrls, or 3dms are found
    find_files(path)
    
    #cross reference wrls/objs to 3dms, remove files from processing 
    #if rhino is already present
    files_to_process = compare_lists(objs, wrls, rhinos)
    
    print files_to_process
    
