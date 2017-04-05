import Rhino
import rhinoscriptsyntax as rs
import imp
import sys

sys.path.append("V:\MeshLab\_FieldSurvey\MK\python\pythonTest\Rhino\HatchUI\Hatch_GUI\hatch_region.py")
sys.path.append("V:\MeshLab\_FieldSurvey\MK\python\pythonTest\Rhino\HatchUI\Hatch_GUI\Hatch_GUI.py")

from DrawModelPaperspace_v2 import PaperDrawing
from hatch_region import hatch_region
from Hatch_GUI import HatchUI
import Hatch_GUI



def main():
    #draw the model
    pd = PaperDrawing()
    pd.run()

    #pick a hatch
    ui = HatchUI()
    ui.show()


if __name__ == "__main__":
    main()