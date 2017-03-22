using System;
using Rhino;
using Rhino.Commands;
using System.Data;
using System.Collections.Generic;

using BVTC.UI.Helpers;
using BVTC.Data.Helpers;
using BVTC;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("76516e05-524f-4bea-bb75-c77e1e39f0cf"),
        CommandStyle(Style.ScriptRunner)]
    public class Submittal : Command
    {
        static Submittal _instance;
        public Submittal()
        {
            _instance = this;
        }

        ///<summary>The only instance of the Submittal command.</summary>
        public static Submittal Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "Submittal"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // find the project number of the current project //
            Data.Project proj = Functions.Find_ProjectInfo(doc);
            if (string.IsNullOrEmpty(proj.ProjectNumber))
            {
                RhinoApp.WriteLine("Could not identify the project number for the current job.");
                return Result.Failure;
            }

            if (!string.IsNullOrEmpty(doc.Path) && doc.Modified)
            {
                RhinoApp.RunScript("!Save ", false);
            }

            // Pull the Drawing list from C-Trac //
            DataTable pdfTable;
            try
            {
                pdfTable = new Repositories.CTrac().Get_PdfList(proj.ProjectNumber);
            }
            catch(BVTC.Repositories.Exceptions.DataMissing e)
            {
                // warn user about error //
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                return Result.Cancel;
            }
            

            UI.DrawingGrid ui = new UI.DrawingGrid(pdfTable);
            Rhino.UI.Dialogs.ShowSemiModal(ui);

            string docPath = doc.Path;
            int submitNumber = -1;
            if (ui.DialogResult == System.Windows.Forms.DialogResult.OK)
            {
                int count = new Repositories.CTrac().CountSubmittals(proj.ProjectNumber);

                if (ui.submittalType == Collections.SubmittalType.New || count == 0)
                {
                    submitNumber = count + 1;
                    RhinoApp.WriteLine("Submittal Number: " + count.ToString());
                }
                else
                {
                    string msg = string.Format("Choose the Submittal to {0}", ui.submittalType);
                    List<string> submittals = new Repositories.CTrac().SubmittalList(proj.ProjectNumber);
                    string result = (string)Rhino.UI.Dialogs.ShowComboListBox(
                        ui.submittalType.ToString(), msg, submittals);
                    Int32.TryParse(result, out submitNumber);

                    // clear the old submittal //
                    if (ui.submittalType == Collections.SubmittalType.Overwrite)
                    {
                        // delete previous submittal info //
                        new Repositories.CTrac().DeleteSubmittal(proj.ProjectNumber, submitNumber);
                    }
                }

                // make sure the correct page settings are applied //
                osTools.PageSettings settings = new osTools.PageSettings(ui.submitTo);

                DataTable dt = ui.dataGrid.Get_CheckedRows();

                int rhinoCol = -1; int pdfCol = -1; int idCol = -1;
                // find rhino and pdf columns in the dataTable //
                for (int i = 0; i < dt.Columns.Count; i++)
                {
                    if (dt.Columns[i].ColumnName == "Path") { rhinoCol = i; }
                    if (dt.Columns[i].ColumnName == settings.PdfColumnName) { pdfCol = i; }
                    if (dt.Columns[i].ColumnName == "GUID") { idCol = i; }
                }

                if (pdfCol < 0)
                {
                    RhinoApp.WriteLine(
                        string.Format("could not find column {0} in data table.",
                        settings.PdfColumnName));
                    return Result.Failure;
                }

                string folder = RhinoTools.FileStructure.SubmittalFolder(
                    doc, submitNumber, ui.submitTo.ToString());
                List<string> pdfs = new List<string>();


                foreach (DataRow row in dt.Rows)
                {
                    string rhinoPath = (string)row[rhinoCol];
                    string pdfPath = (string)row[pdfCol];
                    
                    // parse document guid //
                    Guid id = Guid.Empty;
                    string guid = (string)row[idCol];
                    Guid.TryParse(guid, out id);

                    try
                    {
                        string pdf = RhinoTools.PdfPrinter.UpdatePDF(doc, rhinoPath, pdfPath, settings);
                        osTools.PdfTools.RotatePDF(pdf);
                        if (!string.IsNullOrEmpty(pdf) && id != Guid.Empty)
                        {
                            string cmd = new Repositories.CTrac().Upsert_SubmittalDetail(
                                id, submitNumber, ui.submitTo.ToString());
                            pdfs.Add(pdf);
                        }
                    }
                    catch(Exception e)
                    {
                        Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                    }
                    
                    
                }

                // Update Submittal Header //
                string sqlCmd = new Repositories.CTrac().Upsert_SubmittalHeader(
                    proj.ProjectNumber, submitNumber, ui.submitTo.ToString());


                // combine submittal pdf //
                string combinedPDF = folder + submitNumber.ToString() + "-" + DateTime.Today.CTracFormat() + ".pdf"; 
                osTools.PdfTools.CombinePDFs(pdfs, combinedPDF, true);
                RhinoApp.WriteLine(string.Format(
                    "Created Combined PDF: {0}", combinedPDF ));
                
            }
            else { RhinoApp.WriteLine("Submittal Canceled."); return Result.Cancel; }

            return Result.Success;
        }
    }
}
 