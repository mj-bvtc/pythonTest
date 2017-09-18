import rhinoscriptsyntax as rs
import Rhino
import Hatch_GUI as h
from Hatch_GUI import HatchUI 

def curve_boolean():
    rs.Command("_CurveBoolean _pause")
    curve = rs.LastCreatedObjects()
    print curve
    return curve

def hatch_region(pattern, rotation, scale):
    region = curve_boolean()
    hatches = rs.AddHatches(region, pattern, scale, rotation)
    print hatches
    return region, hatches


def main():
    ui = HatchUI()
    ui.show()
    hatch = ui.selected_hatch
    print hatch.name, hatch.rotation, hatch.scale

    hatch_region(hatch.name, hatch.rotation, hatch.scale)


if __name__ == "__main__":
    main()