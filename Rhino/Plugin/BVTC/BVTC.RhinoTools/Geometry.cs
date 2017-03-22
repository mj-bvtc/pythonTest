using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Rhino;
using Rhino.Geometry;

using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoTools
{
    public class Geometry
    {
        public static Guid BB_Triangle(RhinoDoc doc, Guid id)
        {
            Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);

            // find bb center //
            BoundingBox bb = Get_BoundingBox(doc, id);
            Point3d pt = bb.Center;

            // find bb dimensions //
            double x = bb.Measure_X();
            double y = bb.Measure_Y();

            List<Point3d> ptList = new List<Point3d>();

            // first triangle point //
            Point3d pt0 = new Point3d(pt);
            pt0.X = pt0.X - (x * 1.5);
            pt0.Y = pt0.Y - (y * 0.5);
            ptList.Add(pt0);

            // second triangle point //
            Point3d pt1 = new Point3d(pt);
            pt1.X = pt1.X + (x * 1.5);
            pt1.Y = pt1.Y - (y * 0.5);
            ptList.Add(pt1);

            // thrid triangle point //
            Point3d pt2 = new Point3d(pt);
            pt2.Y = pt2.Y + (y);
            ptList.Add(pt2);

            ptList.Add(pt0);

            Polyline pl = new Polyline(ptList);
            Guid rc = doc.Objects.AddPolyline(pl);

            return rc;
        }

        public static BoundingBox Get_BoundingBox(RhinoDoc doc, Guid id, Plane plane)
        {
            // make sure input Guid was valid //
            if (id == Guid.Empty)
            {
                throw new Exceptions.MissingGUID_Exception("Guid was empty.");
            }

            // try to find the rhino object //
            Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
            if (obj == null)
            {
                throw new Exceptions.MissingGUID_Exception("Cannot find specified object in document.");
            }

            // get base geometry //
            GeometryBase geo = obj.Geometry;

            // return bounding box //
            return geo.GetBoundingBox(plane);
        }
        public static BoundingBox Get_BoundingBox(RhinoDoc doc, List<Guid> ids, Plane plane)
        {
            BoundingBox BB = new BoundingBox();

            for (int i = 0; i < ids.Count; i++)
            {
                BoundingBox bb = Get_BoundingBox(doc, ids[i], plane);
                if (i == 0)
                    BB = bb;
                else
                    BB.Union(bb);
            }

            return BB;
        }
        public static BoundingBox Get_BoundingBox(RhinoDoc doc, List<Guid> ids)
        {
            return Get_BoundingBox(doc, ids, Plane.WorldXY);
        }
        public static BoundingBox Get_BoundingBox(RhinoDoc doc, Guid id)
        {
            return Get_BoundingBox(doc, id, Plane.WorldXY);
        }

        public static double MeasureVolume(RhinoDoc doc, List<Guid> ids, List<string> excludeLayers)
        {
            double volume = 0;

            // get the indexes of all layers to exclude //
            List<int> layerIndexes = new List<int>();
            foreach (string layerName in excludeLayers)
            {
                int index = doc.Layers.FindByFullPath(layerName, true);
                if (index >= 0)
                {
                    layerIndexes.Add(index);
                }
            }

            foreach (Guid id in ids)
            {
                Rhino.DocObjects.RhinoObject geom = doc.Objects.Find(id);
                if((geom.GetType() == typeof(Rhino.DocObjects.BrepObject) || 
                    geom.GetType() == typeof(Rhino.DocObjects.ExtrusionObject))
                    && !layerIndexes.Contains(geom.Attributes.LayerIndex))
                {
                    if (geom.Geometry.HasBrepForm == true)
                    {
                        Brep brep = Rhino.Geometry.Brep.TryConvertBrep(geom.Geometry);
                        if (brep.IsSolid == true)
                        {
                            VolumeMassProperties prop = VolumeMassProperties.Compute(brep);
                            if (prop == null)
                            {
                                throw new Exceptions.BadModeling(
                                    "Could not calculate volume of closed brep, please re-model.");
                            }
                            else
                            {
                                volume += prop.Volume;
                            }
                            
                        }
                    }
                }
            }
            return volume;
        }
        public static double MeasureVolume(RhinoDoc doc, List<Guid> ids)
        {
            // overloaded version to exclude no layers //
            return MeasureVolume(doc, ids, new List<string>());
        }

        public static double MeasureWeight(RhinoDoc doc, List<Guid> ids, List<string> excludeLayers,
            double density, int digits)
        {
            double weight = MeasureVolume(doc, ids, excludeLayers) * density;
            return Math.Round(weight, digits);
        }
        public static double MeasureWeight(RhinoDoc doc, List<Guid> ids)
        {
            double TerraCotta = .082875;
            return MeasureWeight(doc, ids, new List<string>(), TerraCotta, 3);
        }
        public static double MeasureWeight(RhinoDoc doc, List<Guid> ids, List<string> excludeLayers)
        {
            // per cubic inch //
            double TerraCotta = .082875; 
            return MeasureWeight(doc, ids, excludeLayers, TerraCotta, 3);
        }

        public static BVTC.Data.Geometry MeasureGeometry(RhinoDoc doc, List<Guid> ids)
        {
            BVTC.Data.Geometry data = new BVTC.Data.Geometry();

            // get and measure the bounding box //
            BoundingBox bb = Get_BoundingBox(doc, ids);
            data.Length = bb.Measure_X();
            data.Height = bb.Measure_Z();
            data.Depth = bb.Measure_Y();

            // measure volume charectoristics //
            data.Volume = MeasureVolume(doc, ids);
            data.Weight = MeasureWeight(doc, ids);

            return data;
        }

        public Plane PlaneFromFace(BrepFace face)
        {
            AreaMassProperties amp = AreaMassProperties.Compute(face);
            Point3d centroid = amp.Centroid;
            double Uval;
            double Vval;
            face.ClosestPoint(centroid, out Uval, out Vval);
            Vector3d NormalVector = face.NormalAt(Uval, Vval);
            Point3d ptUV = face.PointAt(Uval, Vval);
            Plane plane = new Plane(ptUV, NormalVector);
            Rhino.RhinoApp.WriteLine("Command executed successfully!");
            Rhino.RhinoApp.WriteLine("(Got plane from face)");
            return plane;
        }
        public static Plane PlaneFromFace(BrepFace face, bool makeStatic)
        {
            AreaMassProperties amp = AreaMassProperties.Compute(face);
            Point3d centroid = amp.Centroid;
            double Uval;
            double Vval;
            face.ClosestPoint(centroid, out Uval, out Vval);
            Vector3d NormalVector = face.NormalAt(Uval, Vval);
            Point3d ptUV = face.PointAt(Uval, Vval);
            Plane plane = new Plane(ptUV, NormalVector);
            Rhino.RhinoApp.WriteLine("Command executed successfully!");
            Rhino.RhinoApp.WriteLine("(Got plane from face)");
            return plane;
        }

        public bool isPointOnSurface(RhinoDoc doc, BrepFace face, Point3d point)
        {
            bool result;
            double u;
            double v;
            face.ClosestPoint(point, out u, out v);          //get uv values for closest point
            Point3d closePt = face.PointAt(u, v);          //transform uv point to point3d
            double distToPt = point.DistanceTo(closePt);       //measure distance between points
            if (distToPt > doc.ModelAbsoluteTolerance) { result = false; }
            else { return true; }
            return result;
        }
        public static Curve DuplicateFaceBorder(RhinoDoc doc, BrepFace face)
        {
            Brep f2 = face.DuplicateFace(false);
            Curve[] curves = f2.DuplicateNakedEdgeCurves(true, false); //only trace outside border
            if (curves.Count() == 0) { RhinoApp.WriteLine("No curves found"); return null; }
            curves = Rhino.Geometry.Curve.JoinCurves(curves, doc.ModelAbsoluteTolerance);
            if (curves.Count() == 0) { RhinoApp.WriteLine("Join curves failed"); return null; }
            foreach (var crv in curves)
            {
                //doc.Objects.Add(crv);
            }
            //doc.Views.Redraw();
            RhinoApp.WriteLine("Duplicated border successfully!");
            return curves[0]; //returns first curve, should only be one curve = border
        }
        public Point3d FaceCentroid(RhinoDoc doc, BrepFace face)
        {
            //get centroid
            AreaMassProperties amp = Rhino.Geometry.AreaMassProperties.Compute(face);
            Point3d point = amp.Centroid;
            Rhino.Geometry.Point pt = new Rhino.Geometry.Point(point);
            //doc.Objects.Add(pt);
            return point;
        }//returns point3d, adds point to doc

        public static Point3d FaceCentroid(RhinoDoc doc, BrepFace face, bool makeStatic)
        {
            //get centroid
            AreaMassProperties amp = Rhino.Geometry.AreaMassProperties.Compute(face);
            Point3d point = amp.Centroid;
            Rhino.Geometry.Point pt = new Rhino.Geometry.Point(point);
            //doc.Objects.Add(pt);
            return point;
        }//returns point3d, adds point to doc

        public Point3d CurveCentroid(RhinoDoc doc, Curve curve)
        {
            //get centroid
            AreaMassProperties amp = Rhino.Geometry.AreaMassProperties.Compute(curve);
            Point3d point = amp.Centroid;
            Rhino.Geometry.Point pt = new Rhino.Geometry.Point(point);
            //doc.Objects.Add(pt);
            return point;
        }//returns point3d, adds point to doc
        public Vector3d GetTransVecToOrigin(RhinoDoc doc, Brep brep)
        {
            //get box
            BoundingBox box = brep.GetBoundingBox(true);

            //get minPt
            Point3d minPt = box.Corner(true, true, true);

            //Turn into vector
            Vector3d FromOrigin = new Vector3d(minPt);
            Vector3d ToOrigin = FromOrigin * -1;
            return ToOrigin;
        }
        public void MoveToOrigin(RhinoDoc doc, Brep brep)
        {
            Vector3d toOrigin = GetTransVecToOrigin(doc, brep);
            Transform moveToOrigin = Transform.Translation(toOrigin);
            brep.Transform(moveToOrigin);

        }
        public Curve OffsetCurveFromCentroid(RhinoDoc doc, Curve curve, double distance, bool toCenter)
        {
            double multiplier = 1;
            if (toCenter) { multiplier = 1; }
            else { multiplier = -1; }
            Point3d centroid = CurveCentroid(doc, curve);
            Vector3d normal = doc.Views.ActiveView.ActiveViewport.ConstructionPlane().Normal;
            double tolerance = doc.ModelAbsoluteTolerance;
            CurveOffsetCornerStyle sharp = Rhino.Geometry.CurveOffsetCornerStyle.Sharp;
            Curve[] curves = curve.Offset(centroid * multiplier, normal, distance, tolerance, sharp);
            if (curves.Count() == 0) { return null; }
            return curves[0];

        }
        public Brep Remap(Brep brep, Plane FaceToMap, Plane Destination)
        {
            Transform remap = Transform.PlaneToPlane(FaceToMap, Destination);
            brep.Transform(remap);
            Brep newBrep = (Brep)brep.Duplicate();         
            
            return newBrep;
        }

        public static List<Guid> Remap(List<Guid> objectsToRemap, Plane start, Plane destination, RhinoDoc doc)
        {
            List<Guid> transformedIds = new List<Guid>();  
            Transform remap = Transform.PlaneToPlane(start, destination);
            if(objectsToRemap.Count < 1) { return transformedIds; }
            foreach (var id in objectsToRemap)
            {
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                obj.Geometry.Transform(remap);
                Guid newId = doc.Objects.Add(obj.Geometry);
                transformedIds.Add(newId);
            }
            return transformedIds;
        }

        public static List<Guid> Remap(Guid objectToRemap, Plane start, Plane destination, RhinoDoc doc)
        {
            List<Guid> shortList = new List<Guid> { objectToRemap };
            return Remap(shortList, start, destination, doc);
        }

        public List<GeometryBase> Remap(List<GeometryBase> objects, GeometryBase keyObj, Plane startPlane, Plane destinationPlane)
        {
            //foreach (var geo in objects)
           // {
               
           // }
            return objects;
        }

        public GeometryBase Remap(GeometryBase geo, Plane FaceToMap, Plane Destination)
        {
            Transform remap = Transform.PlaneToPlane(FaceToMap, Destination);
            geo.Transform(remap);
            GeometryBase newGeo = geo.Duplicate();
            return newGeo;
        }
    
        public static void  TransformObjects(List<Guid> objectIds, Transform transform, RhinoDoc doc,  bool copy=false)
        {
            //create empty list to hold objects
            List<GeometryBase> gbList = new List<GeometryBase>();

            foreach (var id in objectIds)
            {
                //get object associated with given guid
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                //obj.Geometry.GetType().IsSubclassOf(typeof(Rhino.Geometry.GeometryBase)); //check if object comes from geometry base
                try
                {
                    //try to coerce object into geometrybase
                    GeometryBase gb = obj.Geometry;

                    //add to list of geometry bases
                    gbList.Add(gb);
                    
                }
                catch {  } //object cannot be converted to gb
                
                
            }
            List<GeometryBase> gbList_old = gbList;
            foreach (var gb in gbList)
            {
                gb.Transform(transform);
                doc.Objects.Add(gb);
            }
            
            if(copy == false)
            {
                foreach (var id in objectIds)
                {
                    doc.Objects.Delete(id, true);
                }
            }

        }

        public static List<GeometryBase> TransformObjects(List<Guid> objectIds, Transform transform, RhinoDoc doc, bool returnGeom, bool copy = false)
        {
            //create empty list to hold objects
            List<GeometryBase> gbList = new List<GeometryBase>();

            foreach (var id in objectIds)
            {
                //get object associated with given guid
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                //obj.Geometry.GetType().IsSubclassOf(typeof(Rhino.Geometry.GeometryBase)); //check if object comes from geometry base
                try
                {
                    //try to coerce object into geometrybase
                    GeometryBase gb = obj.Geometry;

                    //add to list of geometry bases
                    gbList.Add(gb);
                    

                }
                catch { } //object cannot be converted to gb


            }
            List<GeometryBase> gbList_old = gbList;
            List < GeometryBase > gb_new =new  List < GeometryBase >{ };
            foreach (var gb in gbList)
            {
                gb.Transform(transform);
                doc.Objects.Add(gb);
                gb_new.Add(gb);
            }

            if (copy == false)
            {
                foreach (var id in objectIds)
                {
                    doc.Objects.Delete(id, true);
                }
            }
            return gb_new;

        }

        public static List<Guid> TransformObjects(List<Guid> objectIds, Transform transform, RhinoDoc doc, bool returnGeom, bool returnGuidList, bool copy = false)
        {
            //create empty list to hold objects
            List<GeometryBase> gbList = new List<GeometryBase>();

            foreach (var id in objectIds)
            {
                //get object associated with given guid
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                //obj.Geometry.GetType().IsSubclassOf(typeof(Rhino.Geometry.GeometryBase)); //check if object comes from geometry base
                try
                {
                    //try to coerce object into geometrybase
                    GeometryBase gb = obj.Geometry;

                    //add to list of geometry bases
                    gbList.Add(gb);


                }
                catch { } //object cannot be converted to gb


            }
            List<GeometryBase> gbList_old = gbList;
            List<GeometryBase> gb_new = new List<GeometryBase> { };
            List<Guid> guidList_new = new List<Guid>();
            foreach (var gb in gbList)
            {
                gb.Transform(transform);
                Guid id = doc.Objects.Add(gb);
                gb_new.Add(gb);
                guidList_new.Add(id);
            }

            if (copy == false)
            {
                foreach (var id in objectIds)
                {
                    doc.Objects.Delete(id, true);
                }
            }
            return guidList_new;

        }

        public static Vector3d ClosestNormal( Point3d PointNearSurface, BrepFace face)
        {
            double u;
            double v;
            face.ClosestPoint(PointNearSurface, out u, out v);
            Vector3d result = face.NormalAt(u, v);
            return result;
        }
        public static bool IsPointOnSurface(Point3d pointToTest, Surface surf)
        {
            double u;
            double v;
            bool onSurf = surf.ClosestPoint(pointToTest, out u, out v);            

            return onSurf;
        }


        public BVTC.Data.Stock.BrepData bboxOrigin(RhinoDoc doc, Brep brep, BVTC.Data.Stock.BrepData bd)            
        {
            ///Original box, floating in space///
            BoundingBox box = brep.GetBoundingBox(true);
            Point3d[] pts = box.GetCorners();
            Point3d boxZeroPt = pts[0];

            ///translation coordinates, vector///
            double dX = boxZeroPt.X * -1;
            double dY = boxZeroPt.Y * -1;
            double dZ = boxZeroPt.Z * -1;
            Vector3d toOrigin = new Vector3d(dX, dY, dZ);
            Transform to = Transform.Translation(toOrigin);

            ///translate to origin///
            box.Transform(to);
            brep.Transform(to);
            double offset = .5;
            int roundTo = 3;
            Point3d[] ptsOrg = box.GetCorners();
            Point3d ptMax = ptsOrg[6];

            ///calculate value of length, width, height///
            double xval = Math.Ceiling((ptMax.X + (offset * 2)) / roundTo) * roundTo;
            double yval = Math.Ceiling((ptMax.Y + (offset * 2)) / roundTo) * roundTo;
            double zval = (Math.Ceiling((ptMax.Z + offset) / roundTo) * roundTo); //subtract one offset so box stays on origin
            bd.height = (int)zval;
            bd.length = (int)Math.Max(xval, yval);
            bd.width = (int)Math.Min(xval, yval);                                                                                       ///////testing this
            bd.newBottom = brep.Faces[bd.botIndex];                                                     //working on this

            ///make a box from origin with the above dimensions///
            Point3d maxPt = new Point3d(xval, yval, zval);
            BoundingBox newBox = new BoundingBox(ptsOrg[0], maxPt);
            Point3d[] newPts = newBox.GetCorners();
            Line[] lines = newBox.GetEdges();
            foreach (Line line in lines)
            {
                LineCurve ln = new LineCurve(line);
                doc.Objects.Add(ln);
            }

            ///shift block to center of bounding box///
            double xlen = ptMax.X;
            double ylen = ptMax.Y;
            double xshift = (xval - xlen) / 2;
            double yshift = (yval - ylen) / 2;
            Vector3d boxShift = new Vector3d(xshift, yshift, 0);
            Transform middleBox = Transform.Translation(boxShift);
            brep.Transform(middleBox);


            ///Adding Dimensions///

            RefDir rd = new RefDir();
            addDim(doc, newPts[0], newPts[1], rd.negZ * 4);
            addDim(doc, newPts[1], newPts[2], rd.negZ * 4);
            addDim(doc, newPts[0], newPts[4], rd.negX * 4);
            doc.Objects.Add(brep);

            BVTC.Data.Stock.BrepData newData = new BVTC.Data.Stock.BrepData();
            newData.botIndex = bd.botIndex;
            newData.block = brep;
            newData.length = bd.length;
            newData.width = bd.width;
            newData.height = bd.height;

            ///return ///
            return newData;


        }
        public BVTC.Data.Stock.BrepData bboxOrigin(RhinoDoc doc, List<Guid> stuffToMove, BVTC.Data.Stock.BrepData bd)           
        {
            ///Original box, floating in space///
            BoundingBox box = Get_BoundingBox(doc, stuffToMove, Plane.WorldXY);
            Point3d[] pts = box.GetCorners();
            Point3d boxZeroPt = pts[0];

            ///translation coordinates, vector///
            double dX = boxZeroPt.X * -1;
            double dY = boxZeroPt.Y * -1;
            double dZ = boxZeroPt.Z * -1;
            Vector3d toOrigin = new Vector3d(dX, dY, dZ);
            Transform to = Transform.Translation(toOrigin);

            ///translate to origin///
            box.Transform(to);

            List<Guid> movedStuff = TransformObjects(stuffToMove, to, doc, false, true, false);





            double offset = .5;
            int roundTo = 3;
            Point3d[] ptsOrg = box.GetCorners();
            Point3d ptMax = ptsOrg[6];

            ///calculate value of length, width, height///
            double xval = Math.Ceiling((ptMax.X + (offset * 2)) / roundTo) * roundTo;
            double yval = Math.Ceiling((ptMax.Y + (offset * 2)) / roundTo) * roundTo;
            double zval = (Math.Ceiling((ptMax.Z + offset) / roundTo) * roundTo); //subtract one offset so box stays on origin
            bd.height = (int)zval;
            bd.length = (int)Math.Max(xval, yval);
            bd.width = (int)Math.Min(xval, yval);                                                                                       ///////testing this
            bd.newBottom = box.ToBrep().Faces[0];                                                     //working on this

            ///make a box from origin with the above dimensions///
            Point3d maxPt = new Point3d(xval, yval, zval);
            BoundingBox newBox = new BoundingBox(ptsOrg[0], maxPt);
            Point3d[] newPts = newBox.GetCorners();
            Line[] lines = newBox.GetEdges();
            foreach (Line line in lines)
            {
                LineCurve ln = new LineCurve(line);
                doc.Objects.Add(ln);
            }

            ///shift block to center of bounding box///
            double xlen = ptMax.X;
            double ylen = ptMax.Y;
            double xshift = (xval - xlen) / 2;
            double yshift = (yval - ylen) / 2;
            Vector3d boxShift = new Vector3d(xshift, yshift, 0);
            Transform middleBox = Transform.Translation(boxShift);
            


            ///Adding Dimensions///

            RefDir rd = new RefDir();
            addDim(doc, newPts[0], newPts[1], rd.negZ * 4);
            addDim(doc, newPts[1], newPts[2], rd.negZ * 4);
            addDim(doc, newPts[0], newPts[4], rd.negX * 4);
            

            BVTC.Data.Stock.BrepData newData = new BVTC.Data.Stock.BrepData();
            newData.botIndex = bd.botIndex;
            
            newData.length = bd.length;
            newData.width = bd.width;
            newData.height = bd.height;

            ///return ///
            return newData;


        }
        public static List<Guid> bboxOrigin(RhinoDoc doc, List<Guid> stuffToMove)                     //newer version!!!
        {
            ///Original box, floating in space///
            BoundingBox box = Get_BoundingBox(doc, stuffToMove, Plane.WorldXY);
            Point3d[] pts = box.GetCorners();
            Point3d boxZeroPt = pts[0];

            ///translation coordinates, vector///
            double dX = boxZeroPt.X * -1;
            double dY = boxZeroPt.Y * -1;
            double dZ = boxZeroPt.Z * -1;
            Vector3d toOrigin = new Vector3d(dX, dY, dZ);
            Transform to = Transform.Translation(toOrigin);

            ///translate to origin///
            box.Transform(to);

            List<Guid> movedStuff = TransformObjects(stuffToMove, to, doc, false, true, false);



            ///return ///
            return movedStuff;


        }

        public static Transform GetTransformToOrigin(RhinoDoc doc, List<Guid> objIds, bool reverseVec)
        {
            ///Original box, floating in space///
            BoundingBox box = Get_BoundingBox(doc, objIds, Plane.WorldXY);
            Point3d[] pts = box.GetCorners();
            Point3d boxZeroPt = pts[0];

            ///translation coordinates, vector///
            double dX = boxZeroPt.X * -1;
            double dY = boxZeroPt.Y * -1;
            double dZ = boxZeroPt.Z * -1;
            Vector3d toOrigin = new Vector3d(dX, dY, dZ);
            Transform to = Transform.Translation(toOrigin);

            if (reverseVec)
            {
                Vector3d ao = new Vector3d(boxZeroPt.X, boxZeroPt.Y, boxZeroPt.Z);
                Transform awayOrigin = Transform.Translation(ao);
                return awayOrigin;
            }

            else { return to; }
        }

        public void MoveObjectPtToPt(RhinoDoc doc, Brep brep, Point3d start, Point3d end)
        {

            Vector3d dt = new Vector3d(end - start);
            Transform t = Transform.Translation(dt);
            brep.Transform(t);
            return;

        }
        public Rectangle3d MoveRecPtToPt(RhinoDoc doc, Rectangle3d rec, Point3d start, Point3d end)
        {

            Vector3d dt = new Vector3d(end - start);
            Transform t = Transform.Translation(dt);
            rec.Transform(t);
            return rec;

        }
        public Rectangle3d MoveRecPtToPt(Rectangle3d rec, Point3d start, Point3d end)
        {

            Vector3d dt = new Vector3d(end - start);
            Transform t = Transform.Translation(dt);
            rec.Transform(t);
            return rec;

        }
        public Rectangle3d RectangleFromCenter(double width, double length, Point3d pt)
        {
            Plane plane = new Plane(pt, Vector3d.ZAxis);
            Rhino.Geometry.Rectangle3d rec = new Rectangle3d(plane, width, length);
            Rectangle3d movedRec = MoveRecPtToPt(rec, rec.Center, pt);
            return movedRec;
        }
        public class RefDir
        {
            public Vector3d posZ = new Vector3d(0, 0, 1);
            public Vector3d negZ = new Vector3d(0, 0, -1);
            public Vector3d posX = new Vector3d(1, 0, 0);
            public Vector3d negX = new Vector3d(-1, 0, 0);
            public Vector3d posY = new Vector3d(0, 1, 0);
            public Vector3d negY = new Vector3d(0, -1, 0);
        }
        public Point3d MidPt(Point3d a, Point3d b)
        {
            Point3d result = new Point3d();
            result.X = (a.X + b.X) / 2;
            result.Y = (a.Y + b.Y) / 2;
            result.Z = (a.Z + b.Z) / 2;
            return result;
        }

        public void addDim(RhinoDoc doc, Point3d start, Point3d end, Point3d pointOnDimLine)
        {
            double distance = start.DistanceTo(end);
            double offset = start.DistanceTo(pointOnDimLine);
            Plane plane = new Plane(start, end, pointOnDimLine);
            Point2d st = new Point2d(0, 0);
            Point2d ed = new Point2d(distance, 0);
            Point2d of = new Point2d(0, offset);
            LinearDimension dim = new LinearDimension(plane, st, ed, of);
            doc.Objects.AddLinearDimension(dim);
            doc.Views.Redraw();
        }
        public void addDim(RhinoDoc doc, Point3d start, Point3d end, Vector3d PosNegXYZ)
        {
            Point3d midpoint = MidPt(start, end);
            var xform = Rhino.Geometry.Transform.Translation(PosNegXYZ);
            midpoint.Transform(xform);
            Point3d pointOnDimLine = midpoint;
            double distance = start.DistanceTo(end);
            //double offset = start.DistanceTo(pointOnDimLine);
            double offset = PosNegXYZ.Length;
            Plane plane = new Plane(start, end, pointOnDimLine);
            Point2d st = new Point2d(0, 0);
            Point2d ed = new Point2d(distance, 0);
            Point2d of = new Point2d(0, offset);
            LinearDimension dim = new LinearDimension(plane, st, ed, of);
            
            doc.Objects.AddLinearDimension(dim);
            doc.Views.Redraw();
        }

        public static void SilhouetteObjects(RhinoDoc doc, List<Guid> ObjectsToSilhouette)
        {
            foreach (var id in ObjectsToSilhouette)
            {
                Rhino.DocObjects.RhinoObject  obj = doc.Objects.Find(id);
                if(obj.Geometry.HasBrepForm)
                {
                    Brep brep = Brep.TryConvertBrep(obj.Geometry);
                    Curve[] curves = brep.DuplicateEdgeCurves();
                    foreach (var crv in curves)
                    {
                        doc.Objects.Add(crv);
                    }

                }

            }
            doc.Views.Redraw();

        }

        public static double CalculateArea(RhinoDoc doc, Curve curve)
        {
            AreaMassProperties amp = AreaMassProperties.Compute(curve);    //area of offset border
            double area = amp.Area;
            
            return area;
        }





    }
}
