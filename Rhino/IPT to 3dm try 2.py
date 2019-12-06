import rhinoscriptsyntax as rs
import Rhino
import os
import itertools


def find_ipt(file):
    names = set()
    paths = set()
    rhinos = dict()
    for (root, dirs,files) in os.walk(file, topdown=True):
        for f in files:
            if f.upper().endswith("STP"):
                name = f.upper().replace(".IPT.STP", "").replace("TC", "").replace("-", "_")
                #print name
                names.add(name)
                path = os.path.join(root, f)
                paths.add(path)
                rhino = os.path.join(root, name) + ".3dm"
                rhinos[path] = rhino
    return rhinos


def check_3dm(paths):
    rhinos_to_make = dict()
    for p in paths.iteritems():
        if os.path.exists(p[1]):
            print "File exists: {}, skipping".format(p[1])
        else:
            print "Not found: {}, adding to list".format(p[1])
            rhinos_to_make[p[0]] = p[1]
    return rhinos_to_make


def create_3dm(paths):
    count = 1
    for p in paths.iteritems():
        print "Creating file {}: {}".format(count, p[1])
        if count != 0:
            template = rs.TemplateFile()
            cmd="-_New "
            cmd+=template+" "
            cmd+="_Enter "
            rs.Command(cmd)
            cmd="-_Import "
            cmd+='"'+os.path.abspath(p[0])+'"'+" "
            cmd+="_Enter "
            rs.Command(cmd)
            rs.ZoomExtents(all=True)
            cmd="-_SaveAs "
            cmd+='"'+p[1]+'"'+" "
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
    file = r"V:\Projects\120 Stockton\TerraCotta\_Wall Type 3 Benson"
    rhino_list = find_ipt(file)
    rhinos_to_make = check_3dm(rhino_list)
    create_3dm(rhinos_to_make)
    print "finished"

if __name__ == "__main__":
    main()

