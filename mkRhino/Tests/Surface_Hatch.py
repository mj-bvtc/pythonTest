"""Script for hatching on a surface"""

import rhinoscriptsyntax as rs
import Rhino

def hatch_srf():
    # select surfaces
    objs = rs.GetObjects("Select surfaces to hatch", rs.filter.surface, select=True)
    # outline shapes
    rs.Command("_MeshOutline ")
    outlines = rs.LastCreatedObjects()

    # select hatch to use
    for line in outlines:
        rs.AddHatch(line, hatch_pattern="SOLID")
    
    #project hatch onto surface

def hatch_3d():
    objs = rs.GetObjects("Select surfaces to hatch", rs.filter.surface, select=True)
    for obj in objs:
        rs.DuplicateSurfaceBorder(obj, type=1)

def main():
    hatch_3d()
    


if __name__ == "__main__":
    main()