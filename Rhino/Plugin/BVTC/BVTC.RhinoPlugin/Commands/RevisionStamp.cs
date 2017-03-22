using System;
using System.Collections.Generic;

using Rhino;
using Rhino.Commands;

using System.Data;
using System.Windows.Forms;

using BVTC.RhinoTools;
using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("7c097f66-b7a4-45eb-b71e-b8c56f358cc6")]
    public class RevisionStamp : Command
    {
        static RevisionStamp _instance;
        public RevisionStamp()
        {
            _instance = this;
        }

        ///<summary>The only instance of the RevisionStamp command.</summary>
        public static RevisionStamp Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "RevisionStamp"; }
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

            Guid guid = Document.GetGuid(doc, false);

            // get revision table from C-Trac //
            DataTable dt = new Repositories.CTrac().Get_Revisions(guid);

            RhinoApp.WriteLine(string.Format("Column(s): {0}", dt.Columns.Count));
            RhinoApp.WriteLine(string.Format("Rows(s): {0}", dt.Rows.Count));

            // column names //
            foreach (DataColumn col in dt.Columns)
            {
                RhinoApp.WriteLine(col.ColumnName);
            }


            Form revUI = new UI.DisplayDT(dt, "Revision Stamp");
            Rhino.UI.Dialogs.ShowSemiModal(revUI);

            // make sure something was entered //
            if (revUI.DialogResult != DialogResult.OK)
            {
                RhinoApp.WriteLine("Revision changes cancelled.");
                return Result.Cancel;
            }

            // update Revision Table in C-Trac //
            new Repositories.CTrac().Update_RevisionStamp(dt, guid);

            // add text to all layouts //
            foreach (Rhino.Display.RhinoPageView view in views)
            {
                // pull layers to delete //
                List<string> layers = new Repositories.CTrac().Get_LayerNames(
                    this.EnglishName, view.PageName);
                foreach (string layer in layers) { Document.DeleteObjectsByLayer(doc, layer, view); }

                // add revision stamp to document //
                List<Guid> ids = Layout.AddRevisionStamp(doc, view, this.EnglishName, dt);

                // get info for populating text //
                DataTable info = new Repositories.CTrac().Get_TextInformation(
                    this.EnglishName, view.PageName, "Revision");

                // show revision info //
                //Form ui = new UI.DisplayDT(info, "rev info");
                //Rhino.UI.Dialogs.ShowSemiModal(ui);

                string revLetter = new Repositories.CTrac().Get_RevisionLetter(guid);
                
                // create RhinoText object to store all properties //
                RhinoTools.Data.RhinoText text = new RhinoTools.Data.RhinoText(info.Rows[0]);
                text.CreateText(doc, revLetter);

                // get text info from CTrac //
                DataTable textInfo = new Repositories.CTrac().Get_TextInformation(this.EnglishName, view.PageName, "table");
                if (textInfo.Rows.Count > 0)
                {
                    // build table //
                    Layout.Build_RhinoTable(doc, view, dt, "RevisionStamp");
                }
                
            }
            
            // clear empty groups from list //
            Document.ClearEmptyGroups(doc);

            doc.Views.Redraw();
            return Result.Success;
        }
    }
}
