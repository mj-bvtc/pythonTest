import rhinoscriptsyntax as rs
import Rhino
import os


def clear():
    rs.Notes(newnotes="")


def find_rhinos(file):

    paths = set()
    rhinos = dict()
    for (root, dirs,files) in os.walk(file, topdown=True):
        for f in files:
            if f.upper().endswith(".3DM"):
                path = os.path.join(root, f)
                paths.add(path)
    #print paths
    return paths

def clear_all(files):
    count = 1 
    for p in files:
        print "Clearing file {}: {}".format(count, p)
        cmd="-_Import "
        cmd+='"'+os.path.abspath(p)+'"'+" "
        cmd+="_Enter "
        rs.Command(cmd)
        rs.ZoomExtents(all=True)
        clear()
        cmd="-_SaveAs "
        cmd+='"'+p+'"'+" "
        cmd+="_Enter "
        rs.Command(cmd)
        
        cmd="_SelAll "
        cmd="_Delete "
        cmd+="_Enter "
        rs.Command(cmd)
        rs.DocumentModified(False)
        Rhino.RhinoApp.Wait()

        count += 1





def main():
    file = r"V:\Projects\120 Stockton\TerraCotta\_Preliminary_Models\_TEMP"
    rhinos = find_rhinos(file)
    clear_all(rhinos)

if __name__ == "__main__":
    main()