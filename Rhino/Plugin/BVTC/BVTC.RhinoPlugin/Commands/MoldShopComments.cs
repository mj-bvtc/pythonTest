using System;
using System.Data;
using System.Collections.Generic;

using Rhino;
using Rhino.Commands;


using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("1c2c6eb9-aac3-43e5-8a9c-4d1e0cd2078e")]
    public class MoldShopComments : Command
    {
        static MoldShopComments _instance;
        public MoldShopComments()
        {
            _instance = this;
        }

        ///<summary>The only instance of the MoldShopComments command.</summary>
        public static MoldShopComments Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "MoldShopComments"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // get all layouts to revise the same //
            Rhino.Display.RhinoPageView[] views = doc.Views.GetPageViews();
            if (views.Length == 0)
            {
                RhinoApp.WriteLine("Could not add revison stamp, no page layouts exist");
                return Result.Failure;
            }

            // get project number //
            Data.Project proj = new Data.Project();
            proj = Functions.Find_ProjectInfo(doc);
            if (string.IsNullOrEmpty(proj.ProjectNumber))
            {
                RhinoApp.WriteLine("Unable to find project info.");
                return Result.Cancel;
            }

            // get drawing name //
            string drawing = Functions.CurrentDrawing(doc);
            if (string.IsNullOrEmpty(proj.ProjectNumber)) { return Result.Cancel; }

            // get mold comments with project & drawing  //
            DataTable dt = new Repositories.CTrac().Get_MoldShopComments(drawing, proj.ProjectNumber);
            if (dt.Rows.Count == 0)
            {
                RhinoApp.WriteLine("Could not find C-Trac data for drawing: " + drawing);
                return Result.Cancel;
            }

            // set read only columns //
            List<string> readOnly = new List<string>(new string[] { "Block ID" });

            // build UI form //
            System.Windows.Forms.Form ui = new UI.DisplayDT(dt, readOnly, "Mold Shop Comments", false);
            Rhino.UI.Dialogs.ShowSemiModal(ui);

            // Upload modified data to C-Trac //
            int r = new Repositories.CTrac().Update_MoldShopComments(dt, proj.ProjectNumber);

            // create list of data table column headings //
            List<string> headings = dt.GetHeadings(true);

            // try to add oversizing to all avalible layouts
            foreach (Rhino.Display.RhinoPageView view in doc.Views.GetPageViews())
            {
                // set layout to current view //
                RhinoTools.Layout.Set_CurrentView(doc, view.PageName);

                // pull layers that are used by layout
                List<string> layers = new Repositories.CTrac().Get_LayerNames(this.EnglishName, view.PageName);
                
                // delete old oversize stamp //
                foreach (string layer in layers)
                {
                    RhinoApp.WriteLine(layer);
                    RhinoTools.Document.DeleteObjectsByLayer(doc, layer, view);
                }

                // build new oversize table //
                DataTable textInfo = new Repositories.CTrac().Get_TextInformation(this.EnglishName, view.PageName, headings);

                // build Oversize Stamp //
                RhinoTools.Layout.Build_OversizeStamp(doc, dt, textInfo, 0.025);
                doc.Views.Redraw();
            }


            return Result.Success;
        }
    }
}
