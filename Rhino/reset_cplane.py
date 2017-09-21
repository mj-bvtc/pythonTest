import Rhino
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


def reset_cplane():
    rs.Command("'_CPlane _World _Top")



reset_cplane()

