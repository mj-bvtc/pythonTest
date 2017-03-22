using System;
using Rhino;
using Rhino.Commands;
using System.Collections.Generic;
using Rhino.Geometry;
using Rhino.DocObjects;


using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using BVTC.RhinoTools.Helpers;


namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("fee9a784-8eb3-4d32-8486-759501cf6927"), CommandStyle(Style.ScriptRunner)]
    public class BlockExport : Command
    {
        static BlockExport _instance;
        public BlockExport()
        {
            _instance = this;
        }

        ///<summary>The only instance of the BlockExport command.</summary>
        public static BlockExport Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "BlockExport"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            //get objects
            string message = "Choose geometry to become block";
            List<Guid> objects = RhinoTools.Document.GetObjects(doc, message);

            //test isGetObj successful?
            if(objects.Count > 0) { RhinoApp.WriteLine(string.Format("Got {0} objects!", objects.Count.ToString())); }
            else { return Result.Cancel; }

            //create lists to organize objects
            List<Guid> blocks = new List<Guid>();
            List<Guid> otherObjects = new List<Guid>();
            List<Guid> surfaces = new List<Guid>();

            //test if block objects in selection
            foreach (var id in objects)
            {

                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                RhinoApp.WriteLine(obj.ObjectType.ToString());

                //*
                if (obj.ObjectType == Rhino.DocObjects.ObjectType.InstanceReference)
                {
                    RhinoApp.WriteLine("This is a block");
                    blocks.Add(id);
                    //doc.Objects.Hide(id, true);
                }
                else
                {
                    RhinoApp.WriteLine("Good here.");
                    otherObjects.Add(id);
                }
            }

            //explode polysurfaces, add surfaces to list 
            foreach (var id in otherObjects)
            {
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                if (obj.ObjectType == Rhino.DocObjects.ObjectType.PolysrfFilter || obj.ObjectType == Rhino.DocObjects.ObjectType.Surface || obj.ObjectType == Rhino.DocObjects.ObjectType.Brep)
                {
                    Rhino.Geometry.Brep brep = (Rhino.Geometry.Brep)obj.Geometry;
                    if (brep.Faces.Count > 1)
                    {
                        foreach (Rhino.Geometry.BrepFace face in brep.Faces)
                        {
                            Rhino.Geometry.Brep copyFace = face.DuplicateFace(false);
                            Guid faceId = doc.Objects.AddBrep(copyFace);
                            surfaces.Add(faceId);
                        }
                    }
                    else
                    {
                        Rhino.Geometry.BrepFace face = brep.Faces[0];
                        Rhino.Geometry.Brep faceCopy = face.DuplicateFace(false);
                        Guid faceId2 = doc.Objects.Add(faceCopy);
                        surfaces.Add(faceId2);
                    }
                }


                if (obj.ObjectType == Rhino.DocObjects.ObjectType.Extrusion)
                {
                    Rhino.Geometry.Extrusion ext = (Rhino.Geometry.Extrusion)obj.Geometry;
                    if(ext.HasBrepForm)
                    {
                        Rhino.Geometry.Brep brep = ext.ToBrep();
                        if (brep.Faces.Count > 1)
                        {
                            foreach (Rhino.Geometry.BrepFace face in brep.Faces)
                            {
                                Rhino.Geometry.Brep copyFace = face.DuplicateFace(false);
                                Guid faceId = doc.Objects.AddBrep(copyFace);
                                surfaces.Add(faceId);
                            }
                        }
                    }

                }
            }

            //if surface list empty, print message
            foreach (var srf in surfaces)
            {
                RhinoApp.WriteLine(srf.ToString());
            }
            if(surfaces.Count == 0 || otherObjects.Count == 0)
            {
                RhinoApp.WriteLine("No objects converted to blocks");
                return Result.Cancel;
            }
            else
            {
                RhinoApp.WriteLine(string.Format("{0} surfaces total", surfaces.Count.ToString()));
                //foreach (var id in surfaces)
                //{
                    //doc.Objects.Show(id, true);
                //}
            }
            //hide non surfaces
            foreach (var obj in doc.Objects)
            {
                if ( surfaces.Contains(obj.Id))
                {
                    //this is option
                }
                else
                {
                    doc.Objects.Hide(obj.Id, true);
                }
            }


            //select back face
            doc.Views.Redraw();
            Guid backFaceId = RhinoTools.Document.GetObject(doc, "Select back face", false);
            

            //delete other surfaces
            foreach (var id in surfaces)
            {
                if(id != backFaceId)
                { doc.Objects.Delete(id, true); }
            }

            //get normal vector from back surface
            Rhino.DocObjects.RhinoObject obj1 = doc.Objects.Find(backFaceId);
            Rhino.Geometry.Brep brep1 = (Rhino.Geometry.Brep)obj1.Geometry;
            Rhino.Geometry.BrepFace face1 = brep1.Faces[0];
            RhinoTools.Geometry rtg = new RhinoTools.Geometry();
            Rhino.Geometry.Point3d centroid = rtg.FaceCentroid(doc, face1);
            Rhino.Geometry.Vector3d normal = RhinoTools.Geometry.ClosestNormal(centroid, face1);
            doc.Views.Redraw();

            Rhino.Geometry.Plane plane = new Rhino.Geometry.Plane(centroid, normal);


            //delete exploded objects
            doc.Objects.Delete(backFaceId, false);
            RhinoApp.WriteLine("attempted to delete items");

            //remap objects
            Rhino.Geometry.Plane destination = Rhino.Geometry.Plane.WorldZX;
            List<Guid> remappedIds = RhinoTools.Geometry.Remap(otherObjects, plane, destination, doc);
            Transform remapReverse = Transform.PlaneToPlane(destination, plane);

            //move to origin
            List<Guid> stuffAtOrigin = RhinoTools.Geometry.bboxOrigin(doc, remappedIds);
            List<GeometryBase> geomsAtOrigin = new List<GeometryBase>();
            foreach (var id in stuffAtOrigin)
            {
                RhinoObject obj = doc.Objects.Find(id);
                geomsAtOrigin.Add(obj.Geometry);
            }




            //delete other objects
            foreach (var id in objects)
            {
                doc.Objects.Unlock(id, true);
                doc.Objects.Show(id, true);
                doc.Objects.Delete(id, true);
            }


            string displayMessage = "Type in name for block instance";
            string BlockName = RhinoTools.Document.GetUserString(displayMessage);
            string displayMessageDesc = "[Optional] Type in a brief description for block instance";
            if(displayMessageDesc == "") { displayMessageDesc = ""; }
            string BlockDescription = RhinoTools.Document.GetUserString(displayMessageDesc);
            Point3d origin = Point3d.Origin;
            int instanceIndex = doc.InstanceDefinitions.Add(BlockName, BlockDescription, origin, geomsAtOrigin);
            Guid block = doc.Objects.AddInstanceObject(instanceIndex, Transform.Translation(0, 0, 0));
            if (block == Guid.Empty ||string.IsNullOrWhiteSpace(block.ToString()))
            {
                RhinoApp.WriteLine("Instance object not created because block GUID empty");
                return Result.Cancel;
            }

            //get reverse translation
            Transform awayOrigin = RhinoTools.Geometry.GetTransformToOrigin(doc, stuffAtOrigin, true);


            if (stuffAtOrigin.Count>0)
            {
                foreach (Guid id in stuffAtOrigin)
                {
                    doc.Objects.Delete(id, true);
                }
            }
            

            //get reverse transformation to put block where original objects were



            //get project name
            string projectName = "";
            Data.Stock.StockData sd = new Data.Stock.StockData();
            Result getName = Scripts.GetProjectName(sd, doc);
            if(getName == Result.Success)
            {
                projectName = sd.ProjectName;
            }
            else
            {
                return Result.Cancel;
            }

            //assign path for block to be saved to 
            string path = RhinoTools.Document.GetSaveFile(doc);
            //string root = path.ToUpper().Replace(".3DM", "");
            List<string> splits = path.ToUpper().Split('\\').ToList<string>();
            string root = string.Join<string>("\\", splits.GetRange(0, splits.Count - 1));
            string blockString = BlockName.ToString();
            string blockPath = root + "\\" + projectName +  blockString + ".3DM";
            string blockPathB = blockPath.Replace(" ", "");

            //export block to file
            List<Guid> blockList = new List<Guid> { block };
            Result export = BVTC.RhinoPlugin.Commands.Scripts.ExportBlocks(blockList, blockPathB);
            if(export == Result.Success) { }
            else { return Result.Cancel; }

            //update block properties
            string cmd = "-_BlockManager ";
            cmd += "Properties ";
            cmd += blockString + " ";
            cmd += "UpdateType ";
            cmd += "LinkedAndEmbedded ";
            cmd += '"' + blockPathB + '"' + " ";
            cmd += "_Enter ";
            cmd += "_Enter ";
            RhinoApp.WriteLine(cmd);
            bool fixProp = RhinoApp.RunScript(cmd, true);
            if (fixProp) { RhinoApp.WriteLine("Success!"); }
            else { RhinoApp.WriteLine("Failed!"); }


            //add block instance to original location
            
            Guid idNearBeginning = doc.Objects.AddInstanceObject(instanceIndex, awayOrigin);
            //RhinoObject obj2 = doc.Objects.Find(idNearBeginning);
            //obj2.Geometry.Transform(remapReverse);

            
            //delete first block instance
            

            doc.Views.Redraw();
            RhinoApp.WriteLine("end of command");
            return Result.Success;
        }

        
    }
}
