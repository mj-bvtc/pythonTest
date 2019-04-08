
import rhinoscriptsyntax as rs
 
import Rhino.Geometry as rg
from clr import AddReference as addr
addr("Grasshopper")
 
from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
 
 
def raggedListToDataTree(raggedList):
    rl = raggedList
    result = DataTree[object]()
    for i in range(len(rl)):
        temp = []
        for j in range(len(rl[i])):
            temp.append(rl[i][j])
        #print i, " - ",temp
        path = GH_Path(i)
        result.AddRange(temp, path)
    return result
 
def dataTreeToList(aTree):
    theList = []
    for i in range(aTree.BranchCount ):
        thisListPart = []
        thisBranch = aTree.Branch(i)
        for j in range(len(thisBranch)):
            thisListPart.append( thisBranch[j] )
        theList.append(thisListPart)
    return theList


a = dataTreeToList(x)

for i, b in enumerate(a):
    i += 1
    for c in b:
        print "Group {},{}".format(i, c)