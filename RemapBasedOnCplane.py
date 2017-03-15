import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino

#Get mesh
obj = rs.GetObject("Select mesh") 

#Remap mesh to top view
rs.OsnapMode(64)
rs.Command("_CPlane _3Point")        
rs.SelectObject(obj)
rs.Command("RemapCPlane View Front") ###change Front to Top if you want
rs.Command("_SelNone")

####RESET perspective to world top
rs.Command("_SetMaximizedViewport perspective _enter")
rs.Command("'_CPlane _World _Top")
rs.Command("'_4View")
rs.Command("-_Zoom _All _Extents")
