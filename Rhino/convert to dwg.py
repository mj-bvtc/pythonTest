import rhinoscriptsyntax as rs
import Rhino
import os


#get destination folder

#get source folder

#compare .3dm to .dwg

#save any files that need to be saved

folder = rs.BrowseForFolder()
exclude = []
project = "P17-0976"
rhinos = []
for root, dirs, files in os.walk(folder, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for f in files:
        if os.path.splitext(f)[1].upper() == ".3DM":
            if f.startswith(project):
                #print f
                full_path = os.path.join(root,f)
                print full_path
                rhinos.append(full_path)
print 
print

folder = rs.BrowseForFolder()
exclude = []
project = "P17-0976"
autocads = []
for root, dirs, files in os.walk(folder, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for f in files:
        if os.path.splitext(f)[1].upper() == ".DWG":
            if f.startswith(project):
                #print f
                full_path = os.path.join(root,f)
                print full_path
                autocads.append(full_path)

