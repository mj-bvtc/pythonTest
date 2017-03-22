using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input.Custom;
using Rhino.DocObjects;
using System.Windows.Forms;
using Pervasive.Data.SqlClient;
using System.Text.RegularExpressions;
using System.CodeDom.Compiler;
using System.CodeDom;
using System.IO;
using System.Data;
using System.Reflection;
using System.Linq;
using System.Linq.Expressions;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("f091497f-9a19-4628-a0ee-1a85bf5930a6")]
    public class TransformTest : Command
    {
        static TransformTest _instance;
        public TransformTest()
        {
            _instance = this;
        }

        ///<summary>The only instance of the TransformTest command.</summary>
        public static TransformTest Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "TransformTest"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {

            //////////////////////////select objects////////////////////////////////////////////////////////////////////

            BVTC.RhinoTools.Document rTools = new RhinoTools.Document(doc);
            string message = "Select objects to include in stock drawing";
            List<Guid> blockGuids = BVTC.RhinoTools.Document.GetObjects(doc, message);

            //select bottom face + key object (simultaneously)
            BVTC.Data.Stock.Block get_bottom = new Data.Stock.Block();
            get_bottom = rTools.GetFace(doc); //selection
            BrepFace bottom = get_bottom.face; //bottom face
            Guid keyBlockGuid = get_bottom.blockGuid;

            //select front face
            BVTC.Data.Stock.Block get_front = new Data.Stock.Block();           
            get_front = rTools.GetFace(doc); //selection            
            int frontIndex = get_front.faceIndex; //front index, so we can derive front after transformations



            ////////////////////////////create transformations/////////////////////////////////////////////////////

            //Remap
            //bottom
            BVTC.RhinoTools.Geometry rgTools = new RhinoTools.Geometry();
            Plane bottomPlane = rgTools.PlaneFromFace(bottom);
            Plane XY = Plane.WorldXY;
            Transform PlaneToPlane_bottom = Transform.PlaneToPlane(bottomPlane, XY);
            List<Guid> guidList = new List<Guid> {keyBlockGuid };
            List<GeometryBase> geoList =  RhinoTools.Geometry.TransformObjects(guidList, PlaneToPlane_bottom, doc, true, false);
            List<Guid> geoListGuid = RhinoTools.Geometry.TransformObjects(guidList, PlaneToPlane_bottom, doc, false, true, false);
            RhinoTools.Geometry rgt = new RhinoTools.Geometry();

            //front
            GeometryBase newKey = geoList[0];
            Rhino.DocObjects.RhinoObject keyBlock = doc.Objects.Find(keyBlockGuid);
            GeometryBase gb = keyBlock.Geometry; ////////////////////////////////////////////////////////////
            Brep key = (Brep)gb;
            BrepFace newFront = key.Faces[frontIndex]; 
            Plane fPlane = rgTools.PlaneFromFace(newFront);
            Point3d frontPt = new Point3d(newFront.PointAt(0, 0));
            Point fpoint = new Point(frontPt); //draws point on reoriented geometry
            Vector3d normal = fPlane.Normal;
            Vector3d x = Vector3d.XAxis;
            Vector3d z = Vector3d.ZAxis;
            x.Unitize(); //unitizes the living crap out of x
            Vector3d xaxis = z * -1;
            Vector3d yaxis = Rhino.Geometry.Vector3d.CrossProduct(normal, xaxis); //Cross product prevents arbitrary rotation
            Plane newFrontPlane = new Rhino.Geometry.Plane(frontPt, xaxis, yaxis);//reoriented plane with x-axis as rotation control
            Vector3d negY = Vector3d.YAxis * -1;
            Plane xz = new Plane(Point3d.Origin, negY);

            //rotate all geometries to front
            Transform PlaneToPlane_front = Transform.PlaneToPlane(newFrontPlane, xz);   //transform to be used
            //RhinoTools.Geometry.TransformObjects(geoListGuid, PlaneToPlane_front, doc);
            List<Guid> orientedObjList = RhinoTools.Geometry.TransformObjects(geoListGuid, PlaneToPlane_front, doc, false, true, false);

            //Vector3d.VectorAngle()
            

            ////////////////////////////////////////////////////

            //Vector3d motion = new Vector3d(5, 5, 0);
            //Transform translation = Transform.Translation(motion);
            //Point3d origin = Point3d.Origin;
            //Transform scale = Transform.Scale(origin, 3);            
            //Transform both = translation * scale; //multiplication of transformation essentially combines them 
            

            //transform objects
            //RhinoTools.Geometry.TransformObjects(blockGuids, both, doc);
            

            //redraw
            doc.Views.Redraw();





            return Result.Success;
        }
    }
}
