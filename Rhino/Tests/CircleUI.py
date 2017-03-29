import rhinoscriptsyntax as rs
import Rhino
import Meier_UI_Utility


def main():
    ui = CircleUI()
    Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    rs.AddCircle(rs.WorldXYPlane(), ui.radius)



class CircleUI():
    def __init__(self):
        self.radius = 10.0
        self.form = Meier_UI_Utility.UIForm("Circle UI Example")
        self.form.panel.addLabel("", "Radius:", None, False)
        self.form.panel.addNumericUpDown("", 1,50,1,2,self.radius, 80, \
            True, self.Radius_OnValueChange)
        self.form.panel.addLabel("", "Moooo", None, False)
        self.form.layoutControls()
            
            
    def Radius_OnValueChange(self, sender, e):
        self.radius = sender.Value



if __name__ == "__main__":
    main()