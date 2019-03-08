import rhinoscriptsyntax as rs
import Rhino
import uuid


class PaperDrawing:
    """A projection of drawing to modelspace"""
    def __init__(self):
        self.view = rs.CurrentView()
        self.detail = rs.CurrentDetail(self.view)
        self.is_in_detail = None
        self.polysrfs = None
        self.drawing = None
        self.dwg_crvs = None
        self.paper_dwg = None
        self.block_name = None

    def check_in_detail(self):
        type = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport.ViewportType
        if type != Rhino.Display.ViewportType.DetailViewport:
            print "Please enter detail modelspace"
            self.is_in_detail = False
            return
        else:
            self.is_in_detail = True
    
        #get model
    
    def get_objects(self):
        objs = rs.GetObjects("Select objects to draw", filter=28)
        rs.SelectObjects(objs)
        self.polysrfs = objs
        return
    
    def draw_objs(self):
        #make 2d, as current view
        rs.Command("!-_Make2D DrawingLayout=CurrentView _enter _enter")
        self.dwg_crvs = rs.LastCreatedObjects()
        return
    
    def format_block_name(self):
        id = uuid.uuid4()
        name = "PaperDwg_{}_{}_{}".format(self.view, self.detail, id)
        self.block_name = name
        return name

    def add_block(self):
        #cut and paste into view window (paperspace)
        origin = [0,0,0]
        name = self.format_block_name()
        rs.AddBlock(self.dwg_crvs, origin, name, delete_input=True)

    def switch_view(self):
        #leave detail view and insert block
        rs.CurrentDetail(self.view, detail=self.view)
        return
    
    def insert_block(self):
        insert_pt = [17,11,0]
        obj = rs.InsertBlock(self.block_name, insert_pt)
        self.paper_dwg = obj
        return
    
    def orient_block(self):
        #orient 2pt with 3d scaling enabled
        r1 = rs.GetPoint("Pick reference corner 1")
        r2 = rs.GetPoint("Pick reference corner 2")
        t1 = rs.GetPoint("Pick target corner 1")
        t2 = rs.GetPoint("Pick target corner 2")
        ref_pts = [r1, r2]
        target_pts = [t1, t2]
        moved = rs.OrientObject(self.paper_dwg, ref_pts, target_pts, flags=2)
        self.paper_dwg = moved

    def run(self):
        self.check_in_detail()
        if self.is_in_detail is False:
            return
        self.get_objects()
        self.draw_objs()
        self.add_block()
        self.switch_view()
        self.insert_block()
        self.orient_block()
        print "Script Finished"
        return 


def main():
    try:
        pd = PaperDrawing()
        pd.run()
    except Exception:
        print "Something went wrong"

if __name__ == "__main__":
    main()