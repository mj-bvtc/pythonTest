import rhinoscriptsyntax as rs
import Rhino
import Hatch_GUI as h
from Hatch_GUI import HatchUI 

def curve_boolean():
    rs.Command("_CurveBoolean _pause")
    curve = rs.LastCreatedObjects()
    return curve

def hatch_region(pattern, rotation, scale):
    region = curve_boolean()
    rs.AddHatches(region, pattern, scale, rotation)


def main():
    ui = HatchUI()
    ui.txt_path = "V:\MeshLab\_FieldSurvey\MK\python\pythonTest\Rhino\HatchUI\Hatch_GUI\hatches.txt"
    ui.show()
    hatch = ui.selected_hatch

    hatch_region(hatch.name, hatch.rotation, hatch.scale)


if __name__ == "__main__":
    main()