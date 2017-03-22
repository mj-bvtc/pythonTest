using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using System.IO;
using BVTC.Data.Stock;
using System.Data;
using BVTC.Data.Helpers;
using BVTC.RhinoTools.Helpers;
using System.Linq;

namespace BVTC.RhinoPlugin.Commands
{
    class StockFunctions
    {

        //data classes should be instatiated outside of these functions 

        public static Tuple<List<Guid>, NurbsCurve> TransformObjects(RhinoDoc doc, double shrinkage, StockData sd, BrepData bd, Block getBottom, Block getFront, List<Guid> blockGuids)
        {
            try
            {
                ////////////////////////////This tracks transformations ONLY!!!!!!!!////////////////////////////
                shrinkage = 7;




                //Selection//////
                BVTC.RhinoTools.Document rTools = new RhinoTools.Document(doc);
            


                //set data
                bd.blockGuids = blockGuids;
                bd.block = getBottom.block;
                bd.bottom = getBottom.face;
                bd.botIndex = getBottom.faceIndex;
                bd.front = getFront.face;
                bd.frontIndex = getFront.faceIndex;


                //orient block, rescale, translate          
                Point3d origin = Point3d.Origin;
                Vector3d negZ = Vector3d.ZAxis * -1;
                Vector3d negY = Vector3d.YAxis * -1;
                Vector3d x = Vector3d.XAxis;
                Vector3d z = Vector3d.ZAxis;
                Plane xy = new Plane(origin, negZ);
                Plane xz = new Plane(origin, negY);
                BVTC.RhinoTools.Geometry geo = new RhinoTools.Geometry();
                Plane bottomPlane = geo.PlaneFromFace(bd.bottom);


                ///ReOrient bottom face to XY plane///
                Brep orientBottom = geo.Remap(bd.block, bottomPlane, xy); //////this is an object in memory, not doc
                Transform remapA = Transform.PlaneToPlane(bottomPlane, xy);
                BrepFace newfront = orientBottom.Faces[bd.frontIndex]; //references shifted geometry with index from front face
                Plane fPlane = geo.PlaneFromFace(newfront);
                Point3d frontPt = new Point3d(newfront.PointAt(0, 0));
                Point fpoint = new Point(frontPt); //draws point on reoriented geometry
                Vector3d normal = fPlane.Normal;
                x.Unitize(); //unitizes the living crap out of x
                Vector3d xaxis = z * -1;
                Vector3d yaxis = Rhino.Geometry.Vector3d.CrossProduct(normal, xaxis); //Cross product prevents arbitrary rotation
                Plane newPlane = new Rhino.Geometry.Plane(frontPt, xaxis, yaxis);//reoriented plane with x-axis as rotation control


                ///ReOrient front face to XZ plane///
                Brep orientFront = geo.Remap(orientBottom, newPlane, xz);/////object in memory, not doc
                Transform remapB = Transform.PlaneToPlane(newPlane, xz);
                

                ///Scale by Factor///
                double scaleFactor = shrinkage / 100; //turn percent into decimal
                orientFront.Scale(scaleFactor + 1); //adding one scales up by percentage, IE: 7% ----> 1.07 scalefactor
                Transform scale = Transform.Scale(Point3d.Origin, scaleFactor + 1);
                Brep test = orientFront;
                
                
                ///apply previous transformations to original object group selection
                List<Guid> m1 = RhinoTools.Geometry.TransformObjects(blockGuids, remapA, doc, false, true, false);
                List<Guid> m2 = RhinoTools.Geometry.TransformObjects(m1, remapB, doc, false, true, false);
                List<Guid> m3 = RhinoTools.Geometry.TransformObjects(m2, scale, doc, false, true, false);


                //get bound box
                BoundingBox box = RhinoTools.Geometry.Get_BoundingBox(doc, m3);
                Point3d boxZeroPt = box.Corner(true, true, true);
                double dx = boxZeroPt.X * -1;
                double dy = boxZeroPt.Y * -1;
                double dz = boxZeroPt.Z * -1;
                Vector3d toOrigin = new Vector3d(dx, dy, dz);
                Transform to = Transform.Translation(toOrigin);
                List<Guid> returnList;

                //translate to origin                        
                
                test.Transform(to);
                
                List<Guid> newList = RhinoTools.Geometry.TransformObjects(m3, to, doc, false, true, false);
                returnList = newList;
                NurbsCurve curve = DrawStand(doc, getBottom, test);
                //doc.Objects.AddCurve(curve);


                //doc.Objects.AddBrep(test);  //don't addd to document until final transformation complete
                //doc.Objects.AddCurve(curve);

                //wrap up function                
                RhinoApp.WriteLine("Script Complete!!!");
                Tuple<List<Guid>, NurbsCurve> returnTuple = Tuple.Create(returnList, curve);

                doc.Views.Redraw();
                return returnTuple;
            }

            catch { return null; }
        }

        public static Result SaveTemp(RhinoDoc doc)
        {
            string originalPath = doc.Path;
            if (string.IsNullOrEmpty(originalPath) != true) //does file exist
            {
                //if file was saved before, proceed to creating temp file
                System.IO.DirectoryInfo info = new DirectoryInfo(originalPath); //allows for manipulation of file/path
                string tempPath = BVTC.RhinoTools.Helpers.DirectoryInfo_Extensions.GetSaveAs(info, true, "temp"); //  
                return Result.Success;   
            }
            else
            {
                //if doc never saved, first save an original copy then auto create temp file
                RhinoApp.WriteLine("Save an original copy before proceeding: ");
                originalPath = RhinoTools.Document.GetSaveFile(doc);
                System.IO.DirectoryInfo info2 = new DirectoryInfo(originalPath); //must have directory info with updated file
                string tempPath = BVTC.RhinoTools.Helpers.DirectoryInfo_Extensions.GetSaveAs(info2, true, "temp");
                RhinoTools.Document.SaveAs(doc, tempPath);
                return Result.Success;
            }
        }

        public static Result SetData(RhinoDoc doc, StockData sd, BrepData bd, Block getBottom, Block getFront)
        {

            BVTC.RhinoTools.Document rTools = new RhinoTools.Document(doc);



            //set data
            bd.block = getBottom.block;
            bd.bottom = getBottom.face;
            bd.botIndex = getBottom.faceIndex;
            bd.front = getFront.face;
            bd.frontIndex = getFront.faceIndex;


            //get guid            
            sd.GUID = rTools.GetGuid().ToString();


            //get old save location
            string oldSaveLocation = RhinoTools.Document.GetSaveFile(doc);


            //get pnum and pname
            string pname = RhinoTools.FileStructure.Find_ProjectName(doc);          //try to find pname through file structure


            //check if pname empty
            if (string.IsNullOrEmpty(pname))
            {
                UI.ProjectBrowser projectBrowser = new UI.ProjectBrowser(sd);       //use browser to locate pname
                var pbresult = Rhino.UI.Dialogs.ShowSemiModal(projectBrowser);      //this is the result of form showing up
                if (pbresult == System.Windows.Forms.DialogResult.OK )
                {
                    RhinoApp.WriteLine("Got pnum and pname!");
                    sd.ProjectName = projectBrowser.dd.ProjectName;
                    sd.ProjectNumber = projectBrowser.dd.ProjectNumber;
                }
                else { return Result.Cancel; }                                      //cancel if that does not work

            }
            else
            {
                // if function finds result, check if pname is valid
                BVTC.Repositories.CTrac CTrac = new Repositories.CTrac();

                //list of current projects
                string cmd = "CALL Get_Projects()";
                List<string> projects = CTrac.CommandToList(cmd);

                bool isValid = projects.Contains(pname);
                if (isValid)
                {
                    //RhinoApp.WriteLine(pname);
                    RhinoApp.WriteLine("This project exists in CTrac");
                    sd.ProjectName = pname;
                }
                else
                {
                    //RhinoApp.WriteLine(pname);
                    RhinoApp.WriteLine("No projects match in CTrac");
                    return Result.Cancel;                                           //cancel due to bad project
                }
            }      
            
            
            
            
            
                  
            UI.Stock stockui = new UI.Stock(sd);
            var resultstock = Rhino.UI.Dialogs.ShowSemiModal(stockui);
            if (resultstock == System.Windows.Forms.DialogResult.OK)
            {
               
                RhinoApp.WriteLine("worked!!!!");
                sd = stockui.dd; //set final contents from stock ui to local stock dataclass
            }
            else { return Result.Cancel; }                                                      //user cancels ui, cancelling command

            ///saveas, creating new filepath
            ///
            DirectoryInfo info = new DirectoryInfo(doc.Path);
            string newPath = BVTC.RhinoTools.Helpers.DirectoryInfo_Extensions.GetSaveAs(info, false, sd.Part, sd.ProjectNumber);
            RhinoTools.Document.SaveAs(doc, newPath);
            sd.ModelPath = newPath;
            

            return Result.Success;
        }

        public static Result MeasureStock(RhinoDoc doc, List<Guid> blockGuids, Data.Stock.BrepData bd, NurbsCurve curve)
        {
            //get bounding box
            BoundingBox box = RhinoTools.Geometry.Get_BoundingBox(doc, blockGuids);     


            Point3d boxCenter = box.Center;
            Point3d objCenter = box.Center;         ///////use this to center block in inflated box
            objCenter.Z = 0;
            Point3d ptMax = box.Corner(false, false, false);
            Point3d ptMin = box.Corner(true, true, true);
            double offset = .5;
            int roundTo = 3;

            ///calculate value of length, width, height///
            double xval = Math.Ceiling((ptMax.X + (offset * 2)) / roundTo) * roundTo;
            double yval = Math.Ceiling((ptMax.Y + (offset * 2)) / roundTo) * roundTo;
            double zval = (Math.Ceiling((ptMax.Z + offset) / roundTo) * roundTo); //subtract one offset so box stays on origin
            bd.height = (int)zval;
            bd.length = (int)Math.Max(xval, yval);
            bd.width = (int)Math.Min(xval, yval);                                                                                       ///////testing this
            //bd.newBottom = brep.Faces[bd.botIndex];  //don't know why i have this

            //make a new box with inflated dimensions
            Point3d ptMax_inflated = new Point3d(xval, yval, zval);
            BoundingBox box2 = new BoundingBox(Point3d.Origin, ptMax_inflated);
            Point3d box2Center = box2.Center;
            box2Center.Z = 0;

            //Draw edges
            Line[] lines = box2.GetEdges();
            foreach (Line line  in lines)
            {
                LineCurve ln = new LineCurve(line);
                doc.Objects.Add(ln);
            }

            //shift block to center of box
            Vector3d motion = new Vector3d(box2Center - objCenter);
            Transform trans = Transform.Translation(motion);
            RhinoTools.Geometry.TransformObjects(blockGuids, trans, doc, false, true, false);
            curve.Transform(trans);
            doc.Objects.AddCurve(curve);


            //measure stand curve
            BoundingBox curveBox = curve.GetBoundingBox(true);
            double xwidth = curveBox.Measure_X();
            double ylen = curveBox.Measure_Y();
            bd.Stand = string.Join(", ", xwidth.ToString(), ylen.ToString());



            ///Adding Dimensions///
            Point3d[] newPts = box2.GetCorners();
            RhinoTools.Geometry rg = new RhinoTools.Geometry();
            RhinoTools.Geometry.RefDir rd = new RhinoTools.Geometry.RefDir();
            rg.addDim(doc, newPts[0], newPts[1], rd.negY * 4);
            rg.addDim(doc, newPts[3], newPts[0], rd.negX * 4);
            rg.addDim(doc, newPts[5], newPts[1], rd.posX * 4);
           

            return Result.Success;
        }



        public static Result SendData(RhinoDoc doc, StockData sd)
        {
            BVTC.Repositories.CTrac CTrac = new Repositories.CTrac();
            CTrac.Call(
            "InsertStockData",
            sd.Part,
            sd.ProjectNumber,
            sd.UseMold,
            sd.Method,
            sd.StockLength,
            sd.StockWidth,
            sd.StockHeight,
            sd.StockDate,
            sd.PgmDate,
            sd.VerifyDate,
            sd.EMT,
            sd.PartStartDate,
            sd.PartStartTime,
            sd.PartEndDate,
            sd.PartEndTime,
            sd.PartRun,
            sd.PartCompleteDate,
            sd.ModelPath,
            sd.GUID,
            sd.PartPDF,
            sd.StockCut,
            sd.WireCutTraditional,
            sd.Shrinkage);


            return Result.Success;
        }

        public static Result AddLayout(RhinoDoc doc, StockData sd, Rhino.PlugIns.PlugIn PlugIn)
        {
            

            // find all document objects //
            List<Guid> all = RhinoTools.Document.AllObjects(doc);
            
            string layoutName;            

            try { layoutName = "Stock_DWG";}
            catch { layoutName = Interface.GetLayoutName("Stock_DWG", PlugIn); }

            if (layoutName == "") { return Rhino.Commands.Result.Cancel; }

            Rhino.Display.RhinoPageView pageView;

            // try to import layout //
            if (doc.LayoutExists(layoutName) == false)
            {
                string template = RhinoTools.FileStructure.Find_Template(PlugIn);
                RhinoTools.Document.ImportLayout(doc, template, layoutName);

                pageView = RhinoTools.Layout.Set_CurrentView(doc, layoutName);
                RhinoTools.Layout.LockAllDetails(doc, pageView, true);
            }
            else
            {
                pageView = RhinoTools.Layout.Set_CurrentView(doc, layoutName);
            }
            // zoom to selection //            
            RhinoTools.Layout.Details_ZoomExtents(doc, pageView);
            RhinoTools.Layout.Details_ZoomByFactor(doc, pageView, .9);

            // add text to document //
            RhinoTools.Layout.TitleBlockText(doc, sd, pageView, "StockDrawing", true);



            // push data back to C-Trac //


            
    

            doc.Views.Redraw();





            return Result.Success;
        }

        public static Result OrganizeLayers(RhinoDoc doc, StockData sd)
        {
            string option = sd.Method;
            

            RhinoTools.Document.AddLayer(doc, "CNC", System.Drawing.Color.Black);

            switch (option)
            {
                case "CNC":
                    RhinoTools.Document.AddLayer(doc, "CNC::7% Block", System.Drawing.Color.Gold, true);
                    break;

                case "WIRE":
                    RhinoTools.Document.AddLayer(doc, "CNC::7% Block", System.Drawing.Color.LightGreen, true);
                    break;

                case "TRAD":
                    RhinoTools.Document.AddLayer(doc, "CNC::7% Block", System.Drawing.Color.LightSalmon, true);
                    break;


                default:
                    RhinoApp.WriteLine("Method data does not include CNC, WIRE, TRAD as options");
                    break;
            }

            
            RhinoTools.Document.AddLayer(doc, "CNC::Edges", System.Drawing.Color.Black, true);
            RhinoTools.Document.AddLayer(doc, "CNC::Stock", System.Drawing.Color.Black, true);
            RhinoTools.Document.AddLayer(doc, "CNC::Dimensions", System.Drawing.Color.Black, true);
            RhinoTools.Document.AddLayer(doc, "CNC::Stand", System.Drawing.Color.Red, true);
            

            //Rhino.DocObjects.Layer layer = new Rhino.DocObjects.Layer();
            //layer.Color = System.Drawing.Color.Gold;
            //Rhino.DocObjects.Material gold = new Rhino.DocObjects.Material();       
            //gold.SpecularColor = System.Drawing.Color.Gold;
            //Rhino.Render.RenderMaterial goldRender = Rhino.Render.RenderMaterial.CreateBasicMaterial(gold);
            //layer.RenderMaterial = goldRender;
            

            //layer.CommitChanges();

            //assign objects to layers


            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.AnyObject, "7% Block");                //defaults all objects to CNC layer
            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.Annotation, "Dimensions");
            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.Curve, "Edges");
            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.Brep, "7% Block");
            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.Surface, "7% Block");
            RhinoTools.Document.AssignLayerByObjType(doc, Rhino.DocObjects.ObjectType.Detail, "CNC");

            doc.Views.Redraw();


            




            return Result.Success;
        }

        public static NurbsCurve DrawStand(RhinoDoc doc, Data.Stock.Block bottomSelection, Brep brep)
        {
            Guid standGuid = Guid.Empty;
            NurbsCurve blank = new NurbsCurve(null);
            //get bottom index
            int faceIndex = bottomSelection.faceIndex;

            //get key object


            //derive new base
            BrepFace bottom = brep.Faces[faceIndex];

            //outline base
            Curve outline = RhinoTools.Geometry.DuplicateFaceBorder(doc, bottom);


            //offset curve inwards
            RhinoTools.Geometry rtg = new RhinoTools.Geometry();
            Curve offsetOutline = rtg.OffsetCurveFromCentroid(doc, outline, .25, true);

            //get offsetBoundary area
            double offsetArea = RhinoTools.Geometry.CalculateArea(doc, offsetOutline);

            //make empty list for stand options
            //List<RhinoTools.CustomObjects.Standdd> standOptions = new List<RhinoTools.CustomObjects.Standdd>();
            Dictionary<NurbsCurve, double> standOptions = new Dictionary<NurbsCurve, double> { };

            //compare area with available stands
            RhinoTools.CustomObjects.Stands stands = new RhinoTools.CustomObjects.Stands();
            foreach (var std in stands.GetList())
            {
                if(std.area > offsetArea)
                {                    
                    std.areaFits = false;   //does not fit, therefore not an option                                            
                }
                else
                {
                    std.areaFits = true;    //stand fits within bounds, move to testing intersections

                    //center each stand centroid on boundary centroid

                    //edit: draw on boundbox center
                    BoundingBox box = offsetOutline.GetBoundingBox(true);
                    Point3d center = box.Center;
                    center.Z = 0;

                    //Point3d crvCentroid = rtg.CurveCentroid(doc, offsetOutline);
                    Rectangle3d standRectangle = rtg.RectangleFromCenter(std.width, std.length, center);        //rectangle drawn in the middle of crv
                    NurbsCurve rectangle = standRectangle.ToNurbsCurve();

                    //test if any intersections occur, delete any that do
                    double tolerance = doc.ModelAbsoluteTolerance;
                    var result = Rhino.Geometry.Intersect.Intersection.CurveCurve(rectangle, offsetOutline, tolerance, tolerance);
                    if(result.Count > 0) { } //this is not an option, because it intersects
                    else
                    {
                        //add to list of options
                        standOptions.Add(rectangle, std.area);
                    }    
                }
            }

            //use largest block that passes all tests, if there are more than one use first
            if(standOptions.Count > 0)
            {
                bool maxFound = false;
                double maxArea = standOptions.Values.Max();
                foreach (var stand in standOptions)
                {
                    if(maxFound == false && stand.Value == maxArea)
                    {
                        //standGuid = doc.Objects.Add(stand.Key); //add that curve to doc
                        maxFound = true;
                        return stand.Key;
                    }                    
                }                
            }
            else { RhinoApp.WriteLine("No existing stands fit"); }
            //redraw
            doc.Views.Redraw();

            return blank;
        }

        public static void ShiftStep(RhinoDoc doc, Surface surf, int numSteps, int stepMagnitude)
        {
            List<RhinoTools.CustomObjects.Standdd> standOptions = new List<RhinoTools.CustomObjects.Standdd> { };
            RhinoTools.CustomObjects.Stands stands = new RhinoTools.CustomObjects.Stands();
            foreach (var std in stands.GetList())
            {
                std.width += .5; //provides an offset for attaching stand to foam, .25" around the border
                std.length += .5;

                //test in place
                foreach (var point in std.points)
                {
                    if( PointOnSurf(point, surf) == false)
                    {
                        continue;
                    }
                    else
                    {
                        std.numPointsOnSurf += 1;
                        if (std.numPointsOnSurf == 4)
                        {
                            standOptions.Add(std);
                            continue;
                        }
                    }
                }

                //loop through translations in each orthographic direction
             


                //add step
            }

          
        }

        public static bool PointOnSurf(Point3d point, Surface surf)
        {
            return false;
        }

        public static void ReDrawStand(RhinoDoc doc, Block bottom, Brep brep)
        {
            //derive new bottom face from index and shifted brep

            //get bounding box for bottom face

            //align boundBox center with stand center

            //outline outer border of bottom face

            //offset inward .25

            //get area of offsetbaseoutline

            //cull stands whose areas are greater than that of offsetbaseoutline

            //do preliminary removal of stands by trying orthographic shifts from 1-5 inches, seeing if any corner point lies off surface

            //do secondary testing of options by looking for intersections, remove any that intersect

            //remaining bases fit, choose the stand with the largest area, if duplicates arise choose the first instance

            //draw biggest stand if any exist.  If not, throw exception/message "Custom Stand"
            



            return;


        }
        

        public static void ShiftTest(Surface surf, int numSteps, int stepMagnitude)
        {
            Vector3d up = new Vector3d(0, 1, 0);
            Vector3d right = new Vector3d(1, 0, 0);
            Vector3d down = new Vector3d(0, -1, 0);
            Vector3d left = new Vector3d(-1, 0, 0);


            List<RhinoTools.CustomObjects.Standdd> standOptions = new List<RhinoTools.CustomObjects.Standdd> { };
            RhinoTools.CustomObjects.Stands stands = new RhinoTools.CustomObjects.Stands();
            foreach (var std in stands.GetList())
            {
                
            }
            

        }
    }
}
