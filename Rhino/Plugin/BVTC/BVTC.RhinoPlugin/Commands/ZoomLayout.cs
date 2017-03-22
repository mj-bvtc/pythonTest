using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;

using BVTC.Data.Helpers;



namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("47b30124-812d-4621-8ea8-e4e3c71ec555")]
    public class ZoomLayout : Command
    {
        static ZoomLayout _instance;
        public ZoomLayout()
        {
            _instance = this;
        }

        ///<summary>The only instance of the ZoomLayout command.</summary>
        public static ZoomLayout Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "ZoomLayout"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // get the active view //
            Rhino.Display.RhinoView view = doc.Views.ActiveView;
            if (view == null)
                return Rhino.Commands.Result.Failure;
            // check to make sure the current view is a layout //
            Rhino.Display.RhinoPageView pageView = view as Rhino.Display.RhinoPageView;
            if (pageView == null)
            {
                RhinoApp.WriteLine("Active viewport: '{0}' is not a layout", view.MainViewport.Name);
                return Rhino.Commands.Result.Failure;
            }

            // show command line choices for custom scales //
            string msg = "Please selct scaling option for detail views";
            List<string> options = new List<string> { "Auto", "Custom", "Maximum"};
            string choice = Interface.GetString(msg, "Scale", "Auto", options, true);

            double scale = 0;
            if (choice == "Custom")
            {
                //get custom scale for details //
                msg = "Specify scale, in inches per foot";
                string strScale = Interface.GetString(msg, "", "1.5", new List<string>(), true);

                // check to see if the input is a number //
                if (double.TryParse(strScale, out scale) == false || scale <= 0)
                {
                    RhinoApp.WriteLine(string.Format("'{0}' could not be converted valid number", strScale));
                    return Result.Cancel;
                }
                scale = scale / 12;
            }

            // if nothing was entered cancel function //
            if (string.IsNullOrEmpty(choice)) { RhinoApp.Wait(); return Result.Cancel; }

            // save the current active view before running code //
            Rhino.Display.RhinoView reset = doc.Views.ActiveView;

            // update all details of all layouts //
            RhinoTools.Layout.ZoomDetails(doc, pageView, new List<Guid>(), choice, scale);
            RhinoTools.Layout.LockAllDetails(doc, pageView, true);

            // reset view to previous view //
            doc.Views.ActiveView = reset;
            doc.Views.Redraw();

            return Result.Success;
        }
    }
}
