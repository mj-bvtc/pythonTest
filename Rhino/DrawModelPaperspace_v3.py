import rhinoscriptsyntax as rs
import Rhino


class PaperDrawing:
    """A projection of drawing to modelspace"""
    def __init__(self):
        self.view = rs.CurrentView()
        self.scale = None
        self.detail_id = None
        self.get_detail()
        self.detail = rs.CurrentDetail(self.view)
        self.is_in_detail = None
        self.polysrfs = None
        self.drawing = None
        self.dwg_crvs = None
        self.paper_dwg = None
        self.block_name = None



    def get_detail(self):
        self.detail_id = rs.GetObject("Select detail view", rs.filter.detail)
        self.scale = rs.DetailScale(self.detail_id)
        rs.CurrentDetail(self.view, self.detail_id)
        return

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
        objs = rs.GetObjects("Select objects to draw", rs.filter.polysurface)
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

    def scale_block(self):
        origin = [0, 0, 0]
        detail = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.detail_id)
        scale = detail.Geometry.PageToModelRatio
        print scale
        sf = [self.scale, self.scale, self.scale]
        self.block = rs.ScaleObject(self.paper_dwg, origin, sf)

    def move_block(self):
        center = DetailCenter(self.detail_id)
        box = rs.BoundingBox(self.paper_dwg)
        rec = box[0:4]
        rs.MoveObject(self.paper_dwg, center)

    def run(self):
        self.check_in_detail()
        if self.is_in_detail is False:
            return
        self.get_objects()
        self.draw_objs()
        self.add_block()
        self.switch_view()
        self.insert_block()
        self.scale_block()
        self.move_block()
        print "Script Finished"
        return 



###old method
def draw_model_paperspace():
    #go to paperspace, then go to view and enter its modelspace
    view = rs.CurrentView()               #rs.CurrentDetail()
    detail = rs.CurrentDetail(view)

    type = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport.ViewportType
    if type != Rhino.Display.ViewportType.DetailViewport:
        print "Please enter detail modelspace"
        return
    print type


    #get model
    objs = rs.GetObjects("Select objects to draw", rs.filter.polysurface)
    rs.SelectObjects(objs)
    
    
    #make 2d, as current view
    rs.Command("!-_Make2D DrawingLayout=CurrentView _enter _enter")
    dwg_crvs = rs.LastCreatedObjects()
    
    
    #cut and paste into view window (paperspace)
    origin = [0,0,0]
    rs.AddBlock(dwg_crvs, origin, name=view, delete_input=True)
    
    
    #leave detail view and insert block
    rs.CurrentDetail(view, detail=view)
    insert_pt = [17,11,0]
    obj = rs.InsertBlock(view, insert_pt)

    #orient 2pt with 3d scaling enabled
    r1 = rs.GetPoint("Pick reference corner 1")
    r2 = rs.GetPoint("Pick reference corner 2")
    t1 = rs.GetPoint("Pick target corner 1")
    t2 = rs.GetPoint("Pick target corner 2")
    ref_pts = [r1, r2]
    target_pts = [t1, t2]
    rs.OrientObject(obj, ref_pts, target_pts, flags=2)
    
    print "Script Finished"
    return 




def main():

    pd = PaperDrawing()
    pd.run()


if __name__ == "__main__":
    main()