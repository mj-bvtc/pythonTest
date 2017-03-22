using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using System.Data;

using BVTC.UI;
using BVTC.Data.Helpers;
using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("bdbaeb42-fe30-4f19-b486-d58f4c427513")]
    public class EditTitleblock : Command
    {
        static EditTitleblock _instance;
        public EditTitleblock()
        {
            _instance = this;
        }

        ///<summary>The only instance of the EditTitleblock command.</summary>
        public static EditTitleblock Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "EditTitleblock"; }
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

            // save the current active view before running code //
            Rhino.Display.RhinoView reset = doc.Views.ActiveView;

            // get document guid //
            Guid guid = RhinoTools.Document.GetGuid(doc, false);

            // pull drafting data from C-Trac //
            List<Data.Drafting> datalist = Functions.Pull_DraftingData(guid);
            if(datalist.Count == 0)
            {
                RhinoApp.WriteLine("Failed to retrieve any data from C-Trac.");
                return Result.Cancel;
            }
            else
            {
                // edit path with current document location //
                foreach (Data.Drafting data in datalist)
                {
                    data.Path = doc.Path;
                }
            }

            // Build UI //
            string iconFolder = PlugIn.GetBaseFolder() + @"\BVTC.UI\Icons\";
            TitleBlock ui = new TitleBlock(datalist, iconFolder);
            
            Rhino.UI.Dialogs.ShowSemiModal(ui);

            // if dialog was cancelled, return a Result.Cancel //
            if (ui.DialogResult != System.Windows.Forms.DialogResult.OK)
            {
                RhinoApp.WriteLine("UI Canceled, changes not made to  C-Trac.");
                return Result.Cancel;
            }

            // Push data back to C-Trac Pervasive //
            Functions.Push_DraftingData(ui.dataList);

            // build rhino object in layout //
            // create a combined class for text on drawing //
            BVTC.Data.Drafting blockData = (BVTC.Data.Drafting)ui.dataList[0].Duplicate();
            for (int i = 1; i < ui.tabCount; i++)
            {
                blockData.Combine(ui.dataList[i]);
            }

            // add newly updated titleBlock info to all layouts //
            foreach (Rhino.Display.RhinoPageView pageView in doc.Views.GetPageViews())
            {
                // start new layout class //
                RhinoTools.Layout layout = new RhinoTools.Layout(pageView);
                layout.Set_CurrentView();

                // add text to document //
                RhinoTools.Layout.TitleBlockText(doc, blockData, layout.PageView, "Drawing", true);

                if (ui.dataList.Count > 1)
                {
                    List<BVTC.Data.data> generic = ui.dataList.AbstractList();
                    DataTable table = BVTC.Data.DataTools.CompareClasses(generic);



                    // sort column order //
                    table.StripHeadings("Desc");
                    table.AlphabetizeColumns();

                    // build table //
                    layout.Build_RhinoTable(table);
                }
            }
            // reset view to be whatever was set before running command //
            doc.Views.ActiveView = reset;
            doc.Views.Redraw();

            return Result.Success;
        }
    }
}
