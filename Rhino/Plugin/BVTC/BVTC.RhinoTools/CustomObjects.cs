using System;
using System.Collections.Generic;
using Rhino;

using Rhino.Geometry;

using System.Linq;


namespace BVTC.RhinoTools
{
    public class CustomObjects
    {
        public class Stand
        {
            public Stand(BVTC.Data.Stock.StandData d)
            {
                RhinoDoc doc = d.doc;
                RhinoTools.Document mkr = new RhinoTools.Document(doc);
                //GeneralFunctions gf = new GeneralFunctions();

                ///standard settings
                d.edge = .25;
                d.range = 5;
                d.step = 1;

                ///copy geometries
                //Brep newBlock = d.block.DuplicateBrep();
                Brep newBottom = d.bottom.DuplicateFace(false);

                RhinoTools.Geometry geoTools = new RhinoTools.Geometry();

                ///get centroid, does not add to doc
                d.centroid = geoTools.FaceCentroid(doc, newBottom.Faces[0]);

                ///get block border
                Curve border = RhinoTools.Geometry.DuplicateFaceBorder(doc, newBottom.Faces[0]);                              //adds border to memory
                Curve offsetBorder = geoTools.OffsetCurveFromCentroid(doc, border, d.edge, true);        //adds offset to doc
                                                                                                    //doc.Objects.Add(offsetBorder);                                                      //here
                doc.Views.Redraw();
                double borderArea = 0;
                if (offsetBorder.IsClosed && offsetBorder.IsPlanar())
                {
                    AreaMassProperties amp = AreaMassProperties.Compute(offsetBorder);    //area of offset border
                    borderArea = amp.Area;
                }

                


                ///center stands
                Dictionary<Guid, double> recOptions = new Dictionary<Guid, double> { };
                foreach (var dim in d.dimList())
                {
                    Rectangle3d rec = geoTools.RectangleFromCenter(dim.width, dim.length, d.centroid); //add rectangle to memory
                    Rectangle3d newRec = geoTools.MoveRecPtToPt(doc, rec, rec.Center, d.centroid); //move rec to centeroid of block
                    NurbsCurve rectangle = newRec.ToNurbsCurve(); //change to nurbs object
                    Guid recGuid = doc.Objects.Add(rectangle); //add rec to doc, keep track of it with GUID

                    ///see if area of stand is smaller than offset border area
                    if (dim.area < borderArea)
                    {
                        //this is a candidate
                        dim.areaFits = true;
                    }
                    else
                    {
                        dim.areaFits = false;
                    }



                    ///see if rectangle intersects offset border
                    var result = Rhino.Geometry.Intersect.Intersection.CurveCurve(rectangle, offsetBorder, doc.ModelAbsoluteTolerance, doc.ModelAbsoluteTolerance); //check tolerances
                    if (result.Count > 0 || dim.areaFits == false)
                    {
                        RhinoApp.WriteLine("This rect intersects OR is too big!   ----> " + dim.name);
                        RhinoApp.WriteLine("Deleting: " + dim.name);
                        doc.Objects.Delete(recGuid, true);
                    }
                    else
                    {
                        RhinoApp.WriteLine("This rect does not intersect block. -----> " + dim.name);
                        RhinoApp.WriteLine("May be candidate to add");
                        RhinoApp.WriteLine("Border area: " + borderArea.ToString());
                        RhinoApp.WriteLine("Rectangle area: " + rec.Area.ToString());
                        if (borderArea > 0 && borderArea > rec.Area)
                        {
                            recOptions.Add(recGuid, rec.Area);
                            RhinoApp.WriteLine("Adding to list of options");
                        }
                        else
                        {
                            RhinoApp.WriteLine("Didn't meet criteria");
                        }
                    }
                }
                if (recOptions.Count > 0)
                {
                    //Guid BiggestRectangleOption = recOptions.Max();                                                     //error!!!! getting max guid, not max area
                    //foreach (var rec in recOptions)
                    //{
                    //    if(rec != BiggestRectangleOption) //don't delete biggest rec
                    //    { doc.Objects.Delete(rec, true); }//delete all other recs
                    //}

                    double maxArea = recOptions.Values.Max();
                    Guid bigRec;
                    bool maxFound = false;
                    foreach (var pair in recOptions)
                    {

                        if (pair.Value == maxArea && maxFound == false )
                        {
                            bigRec = pair.Key; //set biggest rec   
                            maxFound = true;                         
                        }
                        else
                        {
                            doc.Objects.Delete(pair.Key, true); //delete recs that aren't biggest
                        }
                    }



                }
                else
                {
                    RhinoApp.WriteLine("No stands fit, you must build one!");
                }


            }
        }

        public class Standdd
        {
            public double width { get; set; }
            public double length { get; set; }
            public double area { get; set; }
            public bool flipOrder { get; set; }
            public bool isSquare { get; set; }
            public bool areaFits { get; set; }
            public Point3d center { get; set; }
            public List<Point3d> points { get; set; }
            public int numPointsOnSurf { get; set; }
            public List<Transform> shifts { get; set; }
            

            public Standdd(double dimA, double dimB, bool _flipOrder = false )
            {
                
                area = dimA * dimB;
                width = dimA;
                length = dimB;

                if(dimA == dimB){isSquare = true;}
                else{isSquare = false;}

                if(_flipOrder == true)
                {
                    flipOrder = true;
                    dimA = length;
                    dimB = width;
                }
                else { flipOrder = false; }

                double halfA = width / 2;
                double halfB = length / 2;
                

                center = Point3d.Origin;
                Point3d p1 = new Point3d(halfA, halfB, 0);
                Point3d p2 = new Point3d(halfA * -1, halfB, 0);
                Point3d p3 = new Point3d(halfA * -1, halfB * -1, 0);
                Point3d p4 = new Point3d(halfA, halfB * -1, 0);

                points = new List<Point3d> { p1, p2, p3, p4 };

                Transform up = Transform.Translation(0, 1, 0);
                Transform right = Transform.Translation(1, 0, 0);
                Transform down = Transform.Translation(0, -1, 0);
                Transform left = Transform.Translation(-1, 0, 0);
                shifts = new List<Transform> { up, right, down, left};

            }

        }


        public class Stands
        {
           
            public Standdd A = new Standdd(18, 12);
            public Standdd AA = new Standdd(18, 12, true);
            public Standdd B = new Standdd(6, 12);
            public Standdd BB = new Standdd(6, 12, true);
            public Standdd C = new Standdd(5, 5);
            
            public List<Standdd> GetList()
            {
                List<Standdd> options = new List<Standdd> { A, AA, B, BB, C };
                return options;
            }
            



        }
    

    }
}
