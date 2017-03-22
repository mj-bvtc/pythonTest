using System;
using System.Collections.Generic;
using System.Data;

using Rhino;
using Rhino.Commands;

using BVTC.Data.Helpers;
using BVTC.RhinoTools.Helpers;
using BVTC.RhinoTools.Exceptions;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("831a7330-4faa-4529-81ac-4ca1f1c65e9c"),
        CommandStyle(Style.ScriptRunner)]
    public class AddDrawing : Command
    {
        static AddDrawing _instance;
        public AddDrawing()
        {
            _instance = this;
        }

        ///<summary>The only instance of the AddDrawing command.</summary>
        public static AddDrawing Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "AddDrawing"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // find all document objects //
            List<Guid> all = RhinoTools.Document.AllObjects(doc);

            // get objects to place in drawing //
            List<Guid> objs = RhinoTools.Document.GetObjects(doc, "Select objects to add to drawing.");

            if (objs == null && all.Count == 0)
            {
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }
            if (objs == null)
            {
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }
            // remove selected objects from all //
            if (all.Count > objs.Count)
            {
                foreach (Guid obj in objs)
                {
                    if (all.Contains(obj) == true) { all.Remove(obj); }
                }

                
            }
            else
            {
                all = new List<Guid>();
            }

            // get project data //
            Data.Project projData = new Data.Project();
            try
            {
               projData = RhinoPlugin.Functions.Find_ProjectInfo(doc);
            }
            catch(Exception e)
            {
                // show error to user //
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                RhinoApp.WriteLine("Returning From ProjectInfo Function");
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }


            // get document GUID from notes //
            Guid docID = RhinoTools.Document.GetGuid(doc, false);

            List<BVTC.Data.Drafting> dataList = new List<Data.Drafting>();
            try
            {
                // setup drafting data list //
                dataList = Functions.Pull_DraftingData(docID);
            }
            catch (Exception e)
            {
                // show error to user //
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                RhinoApp.WriteLine("Returning From PullData Function");
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }

            bool newDrawing;

            // measure objects //
            Data.Geometry measurements;
            try
            {
                measurements = RhinoTools.Geometry.MeasureGeometry(doc, objs);
            }
            catch (BadModeling e)
            {
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                RhinoApp.WriteLine(e.Message);
                return Result.Cancel;
            }

            // update data from C-Trac to include current Path //
            if (dataList.Count > 0)
            {
                newDrawing = false;
                foreach (Data.Drafting data in dataList)
                {
                    data.Path = doc.Path;
                    data.Update(measurements);
                }
            }

            // create new blank data class //
            else
            {
                newDrawing = true;
                Data.Drafting data = new Data.Drafting(projData);
                data.User = Functions.GetUser(true);
                data.DateCreated = DateTime.Today;

                // measure objects //
                data.Update(measurements);

                data.GUID = docID.ToString();
                data.Path = doc.Path;
                data.Status = "DRAWN";
                data.Quantity = 1;
                data.CheckedBy = "";
                dataList.Add(data);
            }

            string layoutName = Interface.GetLayoutName("TRADITIONAL", PlugIn);

            if (layoutName == "")
            {
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }

            Rhino.Display.RhinoPageView pageView;
            // try to import layout //
            if (doc.LayoutExists(layoutName) == false)
            {
                string template = RhinoTools.FileStructure.Find_Template(PlugIn);
                RhinoTools.Document.ImportLayout(doc, template, layoutName);

                pageView = RhinoTools.Layout.Set_CurrentView(doc, layoutName);
            }
            else
            {
                pageView = RhinoTools.Layout.Set_CurrentView(doc, layoutName);
            }

            // zoom to selection //
            RhinoTools.Layout.ZoomDetails(doc, pageView, all);
            RhinoTools.Layout.LockAllDetails(doc, pageView, true);

            // build and show TitleBlock UI //
            string iconFolder = PlugIn.GetBaseFolder() + @"\BVTC.UI\Icons\";
            BVTC.UI.TitleBlock ui = new UI.TitleBlock(dataList, iconFolder);
            
            Rhino.UI.Dialogs.ShowSemiModal(ui);

            // add an out in case user does not want update to happen //
            if (ui.DialogResult != System.Windows.Forms.DialogResult.OK)
            {
                RhinoApp.WriteLine("Changes not commited to C-Trac.");

                if (newDrawing == true)
                {
                    // delete drawing //
                    RhinoTools.Document.DeleteLayout(doc, layoutName);
                }
                

                doc.Views.Redraw();
                RhinoApp.Wait();
                return Result.Cancel;
            }

            // create a combined class for text on drawing //
            Data.Drafting blockData = (Data.Drafting)ui.dataList[0].Duplicate();
            for (int i = 1; i < ui.tabCount; i++)
            {
                blockData.Combine(ui.dataList[i]);
            }

            // add text to document //
            RhinoTools.Layout.TitleBlockText(doc, blockData, pageView, "Drawing", true);

            if (ui.dataList.Count > 1)
            {
                // convert list to generic data type then compair //
                List<BVTC.Data.data> generic = ui.dataList.AbstractList();
                DataTable table = BVTC.Data.DataTools.CompareClasses(generic);

                // sort column order //
                table.StripHeadings("Desc");
                table.AlphabetizeColumns();

                // preview data table //
                //Rhino.UI.Dialogs.ShowSemiModal(new DisplayDT(table));
                // build table //
                RhinoTools.Layout.Build_RhinoTable(doc, pageView, table, "Drawing");
            }

            // push data back to C-Trac //
            Functions.Push_DraftingData(dataList);

            // update drafting log //
            Functions.Update_DraftingLog(dataList[0]);

            doc.Views.Redraw();
            RhinoApp.Wait();

            return Rhino.Commands.Result.Success;
        }
    }
}
