import rhinoscriptsyntax as rs
import scriptcontext
import System.Drawing.Color


def SingleColorMesh(MeshID, color):
    MeshObj=rs.coercemesh(MeshID)
    MeshObj.ClearTextureData()
    
    #MeshObj.VertexColors.Clear()
    for i in range(MeshObj.Vertices.Count):
        MeshObj.VertexColors[i] = color
    
    scriptcontext.doc.Objects.Replace(MeshID, MeshObj)
    scriptcontext.doc.Views.Redraw()
    
def Main():
    color = System.Drawing.Color.White
    mesh = rs.GetObject("Select a Mesh", 32)
    if mesh: SingleColorMesh(mesh, color)
    
    
if __name__ == "__main__":
    Main()