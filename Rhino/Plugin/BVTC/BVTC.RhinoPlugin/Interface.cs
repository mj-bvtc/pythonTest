using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino;

using BVTC.RhinoTools.Exceptions;

namespace BVTC.RhinoPlugin
{
    public class Interface
    {
        public static string GetLayoutName(string defaultLayout, Rhino.PlugIns.PlugIn plugin)
        {
            string layoutName;

            // setup command line messages //
            string msg = "Select Layout:";

            // find template file //
            string template = "";
            try
            {
                template = RhinoTools.FileStructure.Find_Template(plugin);
            }
            catch (BVTC.RhinoTools.Exceptions.File_Exception e)
            {
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, "Unable To Locate Template");
                throw e;
            }
            

            // get views from template file //
            List<string> layouts = RhinoTools.Document.GetPageNames(template);
            if (layouts.Count == 0)
            {
                RhinoApp.WriteLine("Cannot locate any layouts from template file.");
                return null;
            }

            // if default string does not exist in layout list //
            if (layouts.Contains(defaultLayout) == false)
                defaultLayout = layouts[layouts.Count - 1];

            // create get string command //
            Rhino.Input.Custom.GetString gs = new Rhino.Input.Custom.GetString();
            gs.AcceptNothing(true);
            gs.SetCommandPrompt(msg);
            gs.SetDefaultString(defaultLayout);
            // add options //
            foreach (string option in layouts)
            {
                gs.AddOption(option);
            }

            // return results //
            Rhino.Input.GetResult r = gs.Get();
            if (r == Rhino.Input.GetResult.Cancel)
                layoutName = "";
            else if (r == Rhino.Input.GetResult.Option)
                layoutName = gs.Option().EnglishName;
            else
                layoutName = gs.StringResult();

            return layoutName;
        }

        public static string GetDrawingName()
        {
            return "User Text";
        }

        public static List<Guid> GetObjects(RhinoDoc doc, string message, int min, int max, bool acceptNothing)
        {

            // get objects to place in drawing //
            Rhino.Input.Custom.GetObject go = new Rhino.Input.Custom.GetObject();

            go.AcceptNothing(acceptNothing);
            if (message != "" && message != null)
                go.SetCommandPrompt(message);

            // get objects //
            Rhino.Input.GetResult result = go.GetMultiple(1, 0);
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

        /// <summary>
        /// Method for requesting string information from Rhino user.
        /// </summary>
        /// <param name="message">string - text to display for user in command line</param>
        /// <param name="defaultString">string -  will populate as default option</param>
        /// <param name="options">string[] - clickable options</param>
        /// <param name="acceptNothing">bool - </param>
        /// <returns>string - result of rhino command line dialog</returns>
        public static string GetString(string message,string name, string defaultString, List<string> options, bool acceptNothing)
        {
            // create custom input class //
            Rhino.Input.Custom.GetString gs = new Rhino.Input.Custom.GetString();

            // allow user to press [esc] to exit //
            gs.AcceptNothing(acceptNothing);

            // display custom message in command prompt //
            if (string.IsNullOrEmpty(message) == false)
                gs.SetCommandPrompt(message);

            // add options list //
            foreach (string option in options)
            {
                RhinoApp.WriteLine(option);
                gs.AddOption(option);
            }

            // set default string for choice //
            if (defaultString != "" && defaultString != null)
                gs.SetDefaultString(defaultString);

            // get input result //
            Rhino.Input.GetResult result = gs.Get();
            if (result == Rhino.Input.GetResult.Cancel)
                return null;
            if (result == Rhino.Input.GetResult.Option)
                return gs.Option().EnglishName;
            return gs.StringResult();

        }
        public static string GetString(string message, bool acceptNothing)
        {
            return GetString(message, "", null, new List<string>(), acceptNothing);
        }

    }
}
