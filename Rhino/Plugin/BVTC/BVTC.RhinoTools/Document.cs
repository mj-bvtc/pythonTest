using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Windows.Forms;
using Rhino.Geometry;
using Rhino;
using Rhino.Commands;
using Rhino.Input.Custom;
using Rhino.DocObjects;
using System.IO;
using BVTC.RhinoTools.Helpers;
namespace BVTC.RhinoTools
{
    public class Document
    {
        /// <summary>
        /// Class to asssist in plugin manipluation of the Rhino Document.
        /// </summary>
        /// <param name="doc"></param>
        public Document(RhinoDoc doc)
        {
            // store doc object in class //
            this.Doc = doc;
        }

        public Rhino.RhinoDoc Doc { get; set; }

        public static string AddLayer(RhinoDoc doc, string layerPath, string parent, System.Drawing.Color color)
        {
            // Parent List //
            List<string> parents = new List<string>();

            // Parent Layer //
            Rhino.DocObjects.Layer parentLayer = Rhino.DocObjects.Layer.GetDefaultLayerProperties();

            // Split layer path into sub layers //
            string[] layerNames = layerPath.Split(new[] { "::" }, StringSplitOptions.None);

            // look up parent layer //
            if (doc.Layers.FindByFullPath(parent, true) < 0)
                if (parent != "")
                    parents.Add(AddLayer(doc, parent, color));
                else
                    parent = "";
            else
                parents.Add(parent);

            //Loop through all child layer from bottom up //
            foreach (string name in layerNames)
            {
                // target layer //
                Rhino.DocObjects.Layer layer = Rhino.DocObjects.Layer.GetDefaultLayerProperties();
                layer.Name = name;
                layer.Color = color;                

                // find parent layer //
                int parentIndex = doc.Layers.FindByFullPath(string.Join("::", parents.ToArray()), true);
                if (parentIndex >= 0)
                {
                    // set parent layer for blank layer //
                    parentLayer = doc.Layers[parentIndex];
                    layer.ParentLayerId = parentLayer.Id;

                }

                // concatinate the full path of layer into a string //
                string fullPath;
                if (parents.Count > 0)
                    fullPath = string.Format("::", parents.ToArray()) + "::" + name;
                else
                    fullPath = name;

                // if layer does not exist, create it //
                if (IsLayer(doc, fullPath) == false)
                {
                    // add layer to document//
                    int layerIndex = doc.Layers.Add(layer);
                    RhinoApp.WriteLine("Created Layer:" + doc.Layers[layerIndex].FullPath);
                }


                // add layer to parent tree //
                parents.Add(name);

            }
            // 
            return string.Join("::", parents.ToArray());
        }

        

        public static string AddLayer(RhinoDoc doc, string layerPath, string parent, string colorStr)
        {
            // overloaded definition with a string color//
            // will return black if it cannot convert string to System.Drawing.Color //
            System.Drawing.Color color = System.Drawing.Color.FromName(colorStr);
            return AddLayer(doc, layerPath, parent, color);
        }
        public static string AddLayer(RhinoDoc doc, string layerPath, string parent)
        {
            return AddLayer(doc, layerPath, parent, System.Drawing.Color.Black);
        }
        public static string AddLayer(RhinoDoc doc, string layerPath, System.Drawing.Color color)
        {
            return AddLayer(doc, layerPath, "", color);
        }
        public static string AddLayer(RhinoDoc doc, string layerPath, System.Drawing.Color color, bool matchRenderColor)
        {
            string layer = AddLayer(doc, layerPath, "", color);
            int layerIndex = doc.Layers.FindByFullPath(layer, true);
            Layer layerobj = doc.Layers[layerIndex];
            Rhino.DocObjects.Material Xcolor = Rhino.DocObjects.Material.DefaultMaterial;
            Xcolor.DiffuseColor = color;            
            Rhino.Render.RenderMaterial xrendercolor = Rhino.Render.RenderMaterial.CreateBasicMaterial(Xcolor);
            int materialIndex = doc.Materials.Add(Xcolor);
            layerobj.RenderMaterial = xrendercolor;
            layerobj.CommitChanges();
            doc.Views.Redraw();

            return layer;
        }
       
        public static string AddLayer(RhinoDoc doc, string layerPath)
        {
            return AddLayer(doc, layerPath, "", "Black");
        }

        public static int AddGroup(RhinoDoc doc, string groupName, int max = 100)
        {
            for (int i = 0; i < max; i++)
            {
                string name;
                // check if group name needs to be incremented up //
                if (i > 0) { name = groupName + i.ToString(); }
                else { name = groupName; }

                // check if group name already exists //
                int index = doc.Groups.Find(name, true);

                // if group does not exist, create it and return index //
                if (index < 0) { return doc.Groups.Add(name); }

                // check if group is empty, if it is use it //
                else
                {
                    if (doc.Groups.GroupObjectCount(index) == 0)
                    {
                        return index;
                    }
                }
            }
            // if too many the max number of attempts was exceeded //
            throw new Exception("Could not create group: " + groupName);
        }

        public static void AddObjectsToGroup(RhinoDoc doc, string groupName, List<Guid> ids)
        {
            // check to make sure the group exists //
            int index = doc.Groups.Find(groupName, true);
            
            if ( index < 0)
            {
                // add the group to the document //
                index = AddGroup(doc, groupName);
            }

            // add each object to the group //
            foreach (Guid id in ids)
            {
                doc.Groups.AddToGroup(index, id);
            }

        }

        public static List<Guid> AllObjects(RhinoDoc doc)
        {
            // Select all objects from a document //

            List<Guid> list = new List<Guid>();

            Rhino.DocObjects.ObjectEnumeratorSettings it = new Rhino.DocObjects.ObjectEnumeratorSettings();
            it.IncludeLights = false;
            it.IncludeGrips = false;
            it.NormalObjects = true;
            it.LockedObjects = true;
            it.HiddenObjects = true;
            it.ReferenceObjects = true;
            IEnumerable<Rhino.DocObjects.RhinoObject> all = doc.Objects.GetObjectList(it);

            foreach (Rhino.DocObjects.RhinoObject item in all)
            {
                list.Add(item.Id);
            }
            return list;
        }

        public static void ClearEmptyGroups(RhinoDoc doc)
        {
            for (int i = 0; i < doc.Groups.Count; i++)
            {
                if (doc.Groups.GroupObjectCount(i) <= 0)
                {
                    doc.Groups.Delete(i);
                }
            }
        }

        public static void DeleteObjectsByLayer(RhinoDoc doc, string layerPath, Rhino.Display.RhinoPageView layout)
        {
            // make sure target layer exists //
            if (IsLayer(doc, layerPath) == false) { RhinoApp.WriteLine("Could not locate:" + layerPath); return; }
            // locate layer index //
            int i = doc.Layers.FindByFullPath(layerPath, true);
            // unlock layer //
            if (doc.Layers[i].IsLocked == true)
                doc.Layers[i].IsLocked = false;

            // get object list //
            Rhino.DocObjects.RhinoObject[] objects = doc.Objects.FindByLayer(doc.Layers[i]);
            if (objects.Length > 0)
            {
                //RhinoApp.WriteLine(string.Format("Delete object(s) from layer: '{0}'", layerPath));
            }

            // create a new empty guid //
            Guid id = Guid.Empty;
            if (layout != null)
                id = layout.ActiveViewportID;

            foreach (Rhino.DocObjects.RhinoObject obj in objects)
            {
                // only delete objects from active page layout//
                if (layout != null)
                {
                    if (obj.Attributes.ViewportId == id)
                    {
                        doc.Objects.Delete(obj.Id, true);
                    }
                }
                else
                {
                    // delete all objects on layer //
                    doc.Objects.Delete(obj.Id, true);
                }
            }
        }
        public static void DeleteObjectsByLayer(RhinoDoc doc, string layerPath)
        {
            // overloaded method to delete all objects on layer in document //
            DeleteObjectsByLayer(doc, layerPath, null);
        }

        public static List<string> GetPageNames(string path, List<string> ignoreViews)
        {
            /* Generate a list showing all layouts in the template file */
            List<string> layoutNames = new List<string>();

            // make sure the template file exists //
            if (System.IO.File.Exists(path) == false) { return layoutNames; }

            // read rhino file //
            Rhino.FileIO.File3dm file = Rhino.FileIO.File3dm.Read(path);

            foreach (Rhino.DocObjects.ViewInfo view in file.Views)
            {
                if (ignoreViews.Contains(view.Name) == false)
                    layoutNames.Add(view.Name);
            }

            // return list of layoutNames //
            return layoutNames;
        }
        public static List<string> GetPageNames(string path)
        {
            List<string> ignoreViews = new List<string>
            { "Top", "Bottom", "Left", "Right", "Front", "Back", "Perspective" };

            return GetPageNames(path, ignoreViews);
        }

        public static Guid GetGuid(RhinoDoc doc, bool save)
        {
            /* Overloaded function to force function to save
             * Get the GUID of the current document.
             * If no GUID exists, generate one.
             */
            Guid guid;
            if (doc.Notes.Length != 36)
            {
                guid = Guid.NewGuid();
                doc.Notes = guid.ToString();
                if (save == true) { RhinoApp.RunScript("!Save", true); }
            }
            else
            {
                Guid.TryParse(doc.Notes, out guid);
            }

            return guid;
        }
        public Guid GetGuid()
        {
            /*
             * Create a unique identifier for a Rhino file.
             * File will need to be saved to commit changes
             * Returns:
             *     guid - 36 charector hexidecimal string
             */
            return GetGuid(this.Doc, false);
        }

        public static bool HasGuid(RhinoDoc doc)
        {
            Guid id = Guid.Empty;
            if (doc.Notes.Length == 36)
            {
                return Guid.TryParse(doc.Notes, out id);
            }
            return false;
        }

        public static List<Guid> GetObjects(RhinoDoc doc, string message, int min, int max, bool acceptNothing)
        {

            // get objects to place in drawing //
            Rhino.Input.Custom.GetObject go = new Rhino.Input.Custom.GetObject();

            go.AcceptNothing(acceptNothing);
            if (message != "" && message != null)
                go.SetCommandPrompt(message);
            
            // get objects //
            Rhino.Input.GetResult result = go.GetMultiple(min, max);
            if (result == Rhino.Input.GetResult.Cancel)
                return null;

            // create list of GUID's //
            Rhino.DocObjects.ObjRef[] objs = go.Objects();
            if (objs == null) { return null; }


            List<Guid> idList = new List<Guid>();
            foreach (Rhino.DocObjects.ObjRef obj in objs)
            {
                idList.Add(obj.ObjectId);
            }

            doc.Objects.UnselectAll(true);
            doc.Views.Redraw();

            return idList;

        }
        public static List<Guid> GetObjects(RhinoDoc doc, string message)
        {
            return GetObjects(doc, message, 0, 9999, true);
        }
        public static Guid GetObject(RhinoDoc doc, string message, bool acceptNothing)
        {
            Guid fail = Guid.Empty;

            // get objects to place in drawing //
            Rhino.Input.Custom.GetObject go = new Rhino.Input.Custom.GetObject();

            go.AcceptNothing(acceptNothing);
            if (message != "" && message != null)
                go.SetCommandPrompt(message);
            go.EnablePreSelect(false, true);
            go.AcceptNothing(false);
            go.SubObjectSelect = true;

            // get objects //
            Rhino.Input.GetResult result = go.Get();
            if (result == Rhino.Input.GetResult.Cancel)
                return fail;

            // create list of GUID's //
            Rhino.DocObjects.ObjRef obj = go.Object(0);
            
            if (obj == null) { return fail; }
            Guid id = obj.ObjectId;
                        
            doc.Objects.UnselectAll(true);
            doc.Views.Redraw();

            return id;
        }

        public static void LayerVisible(RhinoDoc doc, string layer, bool visible)
        {
            if (doc.LayoutExists(layer))
            {
                int index = doc.Layers.FindByFullPath(layer, true);
                doc.Layers[index].IsVisible = visible;
                RhinoApp.WriteLine(doc.Layers[index].Name +" : " + visible.ToString());
            }
            
        }
        public static void LayerVisible(RhinoDoc doc, List<string> layers, bool visible)
        {
            foreach (string layer in layers)
            {
                LayerVisible(doc, layer, visible);
            }
        }

        public static void ImportLayout(RhinoDoc doc, string path, string layoutName)
        {
            // verigfy that all parts exist //
            if (path == null || layoutName == null)
            {
                RhinoApp.WriteLine("Missing path or layoutName.");
                return;
            }

            // get list of current page views //
            string[] existing = doc.GetPageNames();

            // get layouts from template file//
            List<string> layouts = GetPageNames(path);
            RhinoApp.WriteLine("Layout:" + string.Join(",", layouts));

            // import layout into drawing //
            if (layouts.Contains(layoutName) == true)
            {
                if (existing.Contains(layoutName) == false)
                {
                    int index = layouts.IndexOf(layoutName);
                    string cmd = "-_ImportLayout ";
                    cmd += '"' + path + '"' + " ";
                    cmd += (index + 1).ToString() + " ";
                    cmd += "_Enter ";
                    cmd += "_Enter ";

                    bool r = RhinoApp.RunScript(cmd, false);
                }
            }
            else
            {
                throw new Exceptions.Layout_Exception(string.Format(
                    "Could not find PageView: '{0}' in file '{1}'", layoutName, path));
            }
        }

        public static void DeleteLayout(RhinoDoc doc, string layoutName)
        {
            if (doc.LayoutExists(layoutName))
            {
                Layout.Set_CurrentView(doc, layoutName);

                string cmd = "-_CloseViewport Yes _Enter ";
                RhinoApp.RunScript(cmd, false);
            }
        }

        public static bool IsLayer(RhinoDoc doc, string layerPath)
        {
            int i = doc.Layers.FindByFullPath(layerPath, true);
            if (i == -1) { return false; }
            else { return true; }
        }

        public static void LockLayer(RhinoDoc doc, string layerName, bool force)
        {
            if (IsLayer(doc, layerName) == false)
            {
                RhinoApp.WriteLine(string.Format("Layer: '{0}' does not exist to unlock.", layerName));
            }
            int index = doc.Layers.FindByFullPath(layerName, true);

            // Changed to fix bug where layers were not locking //
            Rhino.DocObjects.Layer layer = doc.Layers[index];
            if (layer.IsLocked != force)
            {
                layer.IsLocked = force;
                layer.CommitChanges();
            }
            
        }

        public static bool Set_ColorByObject(RhinoDoc doc, Guid id, System.Drawing.Color color)
        {
            bool r = false;
            try
            {
                Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
                obj.Attributes.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject;
                obj.Attributes.ObjectColor = color;
                obj.Attributes.PlotColor = color;
                obj.Attributes.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromDisplay;
                obj.CommitChanges();

                r = true;
            }
            catch
            {
                RhinoApp.WriteLine("Could not change object color");
            }
            return r;
        }
        public static bool Set_ColorByObject(RhinoDoc doc, Guid id, string color)
        {
            // overload for string input of color //
            return Set_ColorByObject(doc, id, System.Drawing.Color.FromName(color));
        }

        public static bool Set_LayerByObject(RhinoDoc doc, Guid id, int layerIndex)
        {
            bool r = false;
            // locate target object //
            Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(id);
            // set object to layer index //
            obj.Attributes.LayerIndex = layerIndex;
            // commit attribute changes to object //
            obj.CommitChanges();
            r = true;
            return r;
        }
        public static bool Set_LayerByObject(RhinoDoc doc, Guid id, string layerPath)
        {
            // over loaded command to convert layer path to layer index //
            int layerIndex = doc.Layers.FindByFullPath(layerPath, true);
            return Set_LayerByObject(doc, id, layerIndex);
        }
        
        public BVTC.Data.Stock.Block GetFace(RhinoDoc doc)
        {

            BVTC.Data.Stock.Block bb = new BVTC.Data.Stock.Block();

            //get object settings//
            string message = "Select face";
            const ObjectType geometryFilter = ObjectType.Surface;
            GetObject go = new GetObject();
            go.SubObjectSelect = true;
            go.GeometryFilter = geometryFilter;
            go.SetCommandPrompt(message);
            go.EnablePreSelect(false, true);
            go.Get();

            if (go.CommandResult() != Result.Success)
            {
                RhinoApp.WriteLine(go.CommandResult().ToString());
                return null;
            }
            else
            {
                Rhino.RhinoApp.WriteLine("Command executed successfully!");
                Rhino.RhinoApp.WriteLine("Got face with index of: " + go.Object(0).Face().FaceIndex.ToString());
            }
            bb.face = go.Object(0).Face();
            bb.faceIndex = go.Object(0).Face().FaceIndex;
            bb.block = go.Object(0).Brep();
            bb.blockGuid = go.Object(0).ObjectId;
            return bb;
        }
        public static BVTC.Data.Stock.Block GetFace(RhinoDoc doc, bool makeStatic)
        {

            BVTC.Data.Stock.Block bb = new BVTC.Data.Stock.Block();

            //get object settings//
            string message = "Select face";
            const ObjectType geometryFilter = ObjectType.Surface;
            GetObject go = new GetObject();
            go.SubObjectSelect = true;
            go.GeometryFilter = geometryFilter;
            go.SetCommandPrompt(message);
            go.EnablePreSelect(false, true);
            go.Get();

            if (go.CommandResult() != Result.Success)
            {
                RhinoApp.WriteLine(go.CommandResult().ToString());
                return null;
            }
            else
            {
                Rhino.RhinoApp.WriteLine("Command executed successfully!");
                Rhino.RhinoApp.WriteLine("Got face with index of: " + go.Object(0).Face().FaceIndex.ToString());
            }
            bb.face = go.Object(0).Face();
            bb.faceIndex = go.Object(0).Face().FaceIndex;
            bb.block = go.Object(0).Brep();
            bb.blockGuid = go.Object(0).ObjectId;
            return bb;
        }


        public string SaveAs(RhinoDoc doc, string Part, string ProjectNumber)
        {
            //get old path
            string OldPath = GetSaveFile(doc);

            //remove .3dm
            string midPath = OldPath.ToUpper().Replace(".3DM", "");

            //add info to new path
            string newPath = string.Join("_", midPath, Part, ProjectNumber, "CNC.3dm");         //separate by underscore
            string finalPath = newPath.ToUpper().Replace(" ", "");                              //remove spaces

            //save doc as
            RhinoApp.RunScript("_-SaveAs " + finalPath, false);
            RhinoApp.WriteLine("SavedAs:   " + finalPath);

            //return new filepath
            return finalPath;

        }
        public static void SaveAs(RhinoDoc doc, string newFilePath)
        {
            RhinoApp.RunScript("_-SaveAs " + newFilePath, false);
        }

        public static string GetSaveFile(RhinoDoc doc)
        {
            //checks if doc is null or empty, if either is true, it will be saved and the filepath will exist//
            if (doc.Path == null || doc.Path.Length == 0)
            {
                var sfd = new SaveFileDialog();
                sfd.DefaultExt = ".3dm";
                sfd.Filter = "Rhino Files (*.3dm)|.3dm";
                sfd.Title = "Save a Rhino File";
                sfd.CheckPathExists = true;
                if (sfd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    RhinoApp.RunScript("_-SaveAs " + sfd.FileName, false);
                }
            }
            string filepath = doc.Path;
            return filepath;
        }
        
        public bool isSaved(RhinoDoc doc)
        {
            //set a boolean
            bool saveStatus = false;

            //save location to test
            string file = doc.Path;

            //test if there is a value or not
            if (string.IsNullOrEmpty(file))
            {
                saveStatus = false;
            }
            else
            {
                saveStatus = true;
            }

            //return result
            return saveStatus;
        }
        
        public Tuple<double, double, double> GetBoundingBoxDimensions(RhinoDoc doc, Brep brep)
        {

            //move to origin
            BVTC.RhinoTools.Geometry geo = new Geometry();
                
                geo.MoveToOrigin(doc, brep);

            //add bounding box
            BoundingBox box = brep.GetBoundingBox(true);

            //get max pt
            Point3d maxPt = box.Corner(false, false, false);

            //set dims to W, L, H
            double height = maxPt.Z;
            double length = Math.Max(maxPt.X, maxPt.Y);
            double width = Math.Min(maxPt.X, maxPt.Y);

            //return tuple
            Tuple<double, double, double> dims = Tuple.Create(width, length, height);
            return dims;


        }
        public Guid ObjGuid(RhinoDoc doc, RhinoObject obj)
        {
            Guid id = obj.Id;
            return id;
        }

        public static void ChangeObjLayer(RhinoDoc doc, Rhino.DocObjects.RhinoObject obj, string fullLayerPath)
        {
            
            int layerIndex = doc.Layers.Find(fullLayerPath, true);
            obj.Attributes.LayerIndex = layerIndex;
            obj.CommitChanges();
        }

        public static void AssignLayerByObjType(RhinoDoc doc, Rhino.DocObjects.ObjectType ot, string fullLayerPath)
        {
            Rhino.DocObjects.RhinoObject[] objs = doc.Objects.FindByObjectType(ot);
            foreach (var obj in objs)
            {
                ChangeObjLayer(doc, obj, fullLayerPath);
            }

        }


        public static string GetUserString(string DisplayMessage, bool acceptNothing = false)
        {
            Rhino.Input.Custom.GetString gs = new Rhino.Input.Custom.GetString();
            string strResult = "Operation Cancelled";
            gs.AcceptNothing(acceptNothing);
            gs.SetCommandPrompt(DisplayMessage);
            //gs.AcceptCustomMessage(true);
            Rhino.Input.GetResult result = gs.GetLiteralString();
            //Rhino.Input.GetResult result = gs.Get();
            if (result == Rhino.Input.GetResult.Cancel)
            {
                return strResult;
            }
            else 
            {
                strResult = gs.StringResult();
            }
            return strResult;
        }

    }
}
