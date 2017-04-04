import rhinoscriptsyntax as rs
import Rhino
import ghpythonlib.parallel
import time, math
import scriptcontext
#import utility as rs
import System.Drawing.Color
import os
import Meier_UI_Utility 
import Meshlab_Tools as mt

def Build_Key(Point,colors,tol):
    """
    Build key for tolerance shading.
    Create color coded text objects and planes.
    """
    low2="-"+str(tol[2])+'"'+" and lower"
    low1="-"+str(tol[2])+'"'+" to -"+str(tol[1])+'"'
    low0="-"+str(tol[1])+" to -"+str(tol[0])+'"'
    good="-"+str(tol[0])+" to +"+str(tol[0])+'"'
    high0="+"+str(tol[0])+" to +"+str(tol[1])+'"'
    high1="+"+str(tol[1])+" to +"+str(tol[2])+'"'
    high2="+"+str(tol[2])+" and higher"
    
    stringList=[high2,high1,high0,good,low0,low1,low2]
    objs=[]
    for i in range(len(stringList)):
        pt=rs.coerce3dpoint([0,0,1.5*i+3])
        plane=rs.PlaneFromNormal(pt+Point,[0,-1,0],[1,0,0])
        txt=rs.AddText(stringList[i],plane)
        srf=rs.AddPlaneSurface(plane,1,1)
        rs.MoveObject(srf,[-2,0,0])
        stringColor="Tol_"+colors[i].ToString().split("[")[1].rstrip("]")
        
        mt.OrganizeLayer(stringColor,Objects=[srf, txt],Render=colors[i],Color=colors[i])
        
        ## Maybe Later add rectangle around text ##
        #objs.append(txt)
        #objs.append(srf)

def ColorMesh(MeshID,BlockID):
    MeshObj=rs.coercemesh(MeshID)
    MeshObj.EnsurePrivateCopy()
    
    Brep=rs.coercegeometry(BlockID)
    Brep.EnsurePrivateCopy()
    
    BB=rs.BoundingBox(BlockID)
    bb=rs.coerceboundingbox(BB).ToBrep()
    bb.EnsurePrivateCopy()
    
    time1a = time.time()    #Start Timer
    
    tol=scriptcontext.doc.ModelAbsoluteTolerance
    
    Red=rs.coercecolor(System.Drawing.Color.Red)            ## Too Low ##
    Orange=rs.coercecolor(System.Drawing.Color.Orange)
    Yellow=rs.coercecolor(System.Drawing.Color.Yellow)
    Green=rs.coercecolor(System.Drawing.Color.Green)        ## Within Tol ##
    LtBlue=rs.coercecolor(System.Drawing.Color.LightBlue)
    Blue=rs.coercecolor(System.Drawing.Color.Blue)
    Purple=rs.coercecolor(System.Drawing.Color.Purple)      ## Too High ##
    
    White=rs.coercecolor(System.Drawing.Color.White)
    
    
    Colors=[Purple,Blue,LtBlue,Green,Yellow,Orange,Red]
    ##  \/ Set Tolerances Here \/ ##
    Range=[1/32,1/16,1/8]
    
    Build_Key(BB[5],Colors,Range)
    
    Rhino.RhinoApp.Wait()
    
    ColorList=range(MeshObj.Vertices.Count)
    
    def CalculateColor(i):
        Vertex=MeshObj.Vertices[i]
        Point=rs.coerce3dpoint(Vertex)
        
        if bb.IsPointInside(Point,tol,True)==False:
            Color = White
            
        else:
            CP=Brep.ClosestPoint(Point)
            Distance=Point.DistanceTo(CP)
            Color=None 
            
            if Distance<Range[0]:
                Color=Colors[3] # Green #
            
            elif Distance<Range[1]:
                if Brep.IsPointInside(Point,tol,True)==True:
                    Color=Colors[4] #Too Low
                else:
                    Color=Colors[2] #Too High
            
            elif Distance<Range[2]:
                if Brep.IsPointInside(Point,tol,True)==True:
                    Color=Colors[5] #Too Low
                else:
                    Color=Colors[1] #Too High
            
            # Outside Range #
            else:
                if Brep.IsPointInside(Point,tol,True)==True:
                    Color=Colors[6] #Too Low
                else:
                    Color=Colors[0] #Too High
        
        
        ColorList[i]=Color
        
    
    print MeshObj.Vertices.Count
    ghpythonlib.parallel.run(CalculateColor,range(MeshObj.Vertices.Count))
    
    for Color in ColorList:
         MeshObj.VertexColors.Add(Color)
    
    scriptcontext.doc.Objects.Replace(MeshID, MeshObj)
    scriptcontext.doc.Views.Redraw()
    
    ## Add Scale ##
    time1b = time.time()    #End Timer
    print round(time1b - time1a, 3)


def ScanCompair():
    
    mesh = rs.GetObject("Select Scan Data:",32)
    if not mesh: return
    block = rs.GetObject("Select Closed Polysurface to Compair:",16)
    if not block: return
    if not rs.IsPolysurfaceClosed(block):
        print "Polysurface is not closed"
        return
    
    ColorMesh(mesh,block)
    
    rs.HideObject(block)
    
    cmd="-_SetDisplayMode "
    cmd+="Viewport=Active "
    cmd+="Mode=Shaded "
    cmd+="_Enter "
    
    rs.Command(cmd)
    

if __name__ == "__main__":
    ScanCompair()
    
    #Main()

