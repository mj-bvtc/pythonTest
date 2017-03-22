using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Windows.Forms;
using Rhino;
using BVTC.Data.Exceptions;
using BVTC.Repositories.Exceptions;


namespace BVTC.RhinoPlugin
{
    /// <summary>
    ///  Functions that can be reused within the RhinoPlugin
    /// </summary>
    class Functions
    {
        public static List<Data.Drafting> Pull_DraftingData(Guid guid)
        {
            // create data list //
            List<BVTC.Data.Drafting> datalist = new List<BVTC.Data.Drafting>();

            // create connection to C-Trac //
            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
            DataTable dt = new DataTable();

            try
            {
                CTrac.OpenDB();
                RhinoApp.WriteLine(string.Format("CALL DraftingDataByGUID('{0}')", guid.ToString()));
                dt = CTrac.CommandToDataTable(string.Format("CALL DraftingDataByGUID('{0}')", guid.ToString()));
            }
            finally
            {
                CTrac.CloseDB();
            }

            foreach (DataRow row in dt.Rows)
            {
                BVTC.Data.Drafting data = new BVTC.Data.Drafting(row);
                datalist.Add(data);
            }
            return datalist;
        }

        public static void Push_DraftingData(List<Data.Drafting> dataList)
        {
            // fix this to open and close connection to C-Trac //
            try
            {
                foreach (BVTC.Data.Drafting data in dataList)
                {
                    string sqlCmd = data.UpsertCTrac();
                    //RhinoApp.WriteLine(sqlCmd);
                }
            }
            catch (Exception e)
            {
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
            }
        }

        public static void Update_DraftingLog(Data.Drafting data)
        {
            // create connection to C-Trac //
            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");

            try
            {
                CTrac.OpenDB();

                string sqlCmd = string.Format("CALL Update_DraftingLog('{0}', '{1}', '{2}')", data.ProjectNumber, data.BaseStyle, data.User);
                RhinoApp.WriteLine(sqlCmd);
                CTrac.ExecuteCommand(sqlCmd);
            }
            catch (Exception e)
            {
                throw e;
            }
            finally
            {
                CTrac.CloseDB();
            }
        }

        public static Data.Project Find_ProjectInfo(RhinoDoc doc)
        {
            /* Attempt to find project data 
             *      -Project Number
             *      -Short Description
             */
            BVTC.Data.Project data = new BVTC.Data.Project();
            string projNum = "";
            string projName = "";

            if (RhinoTools.Document.HasGuid(doc))
            {
                // get project number from the guid //
                Guid id = RhinoTools.Document.GetGuid(doc, false);
                projNum = new Repositories.CTrac().Get_ProjectNumber(id);
                if (string.IsNullOrEmpty(projNum) == false)
                {
                    projName = new Repositories.CTrac().Get_ProjectName(projNum);
                }
            }

            if (string.IsNullOrEmpty(projNum) || string.IsNullOrEmpty(projName))
            {
                // use  file naming standards to find project name and folder location //
                string projFolder = RhinoTools.FileStructure.Find_ProjectFolder(doc);
                projName = RhinoTools.FileStructure.Find_ProjectName(doc);

                // check it project folder is correctly named //
                projNum = new Repositories.CTrac().Get_ProjectNumber(projName);
            }
            

            if (string.IsNullOrEmpty(projNum) || string.IsNullOrEmpty(projName))
            {
                // get list of all avalible project names from C-Trac //
                List<string> projectNames = new Repositories.CTrac().Get_ShortDescriptions();

                UI.ProjectInfo ui = new UI.ProjectInfo(doc, projName);

                Rhino.UI.Dialogs.ShowSemiModal(ui);
                RhinoApp.Wait();

                if (ui.DialogResult == DialogResult.OK)
                {
                    data.ProjectNumber = ui.ProjectNumber;
                    data.ShortDescription = ui.ProjectName;
                }
                else
                {
                    throw new Exception("Project Name/Number not specified.");
                }
            }
            else
            {
                data.ShortDescription = projName;
                data.ProjectNumber = projNum;
            }

            
            if (string.IsNullOrEmpty(data.ProjectNumber) || string.IsNullOrEmpty(data.ShortDescription))
            {
                // throw exception if failed to find //
                throw new Exception("Could not find project data");
            }

            return data;
        }

        public static string GetUser(bool popup)
        {
            string user = new Repositories.CTrac().Get_CurrentUser();

            // giver user manuel entry message box //
            if (user == "" && popup == true)
            {
                string message = string.Format("Cannot locate '{0}' in directory.  Enter your initials.", Environment.UserName);
                string title = "Locate User";
                Rhino.UI.Dialogs.ShowEditBox(title, message, "", false, out user);
                RhinoApp.Wait();
            }

            return user.ToUpper();
        }

        public static string CurrentDrawing(RhinoDoc doc)
        {
            // try to get drawing from document guid //

            string drawing = new Repositories.CTrac().Get_Drawing(RhinoTools.Document.GetGuid(doc, false));
            if (new Repositories.CTrac().DrawingExists(drawing) == true)
            {
                return drawing;
            }
            else { drawing = ""; }

            // if still unable to get a drawing name //
            if (string.IsNullOrEmpty(drawing) && string.IsNullOrEmpty(doc.Name) == false)
            {
                // remove .3dm from doc.name for parsing //
                string name = doc.Name.Substring(0, doc.Name.Length - 4);

                // Block Export Naming Style //
                // Example: P14-0509_CS1.3dm //
                if (name.Length > 4)
                {
                    if (name[0] == 'P' && name[3] == '-' && name.Contains('_'))
                    {
                        int index = name.IndexOf('_');
                        string test = name.Substring(index + 1, name.Length - index - 1);
                        if (new Repositories.CTrac().DrawingExists(test) == true)
                        {
                            return test;
                        }
                    }
                }
                // check if lateral drawing name is file name //
                else if (new Repositories.CTrac().DrawingExists(name) == true)
                {
                    return name;
                }
            }

            // unable to automatically determain drawing number, ask user to enter manually //
            drawing = Interface.GetString("Specify Drawing Number", true);

            // check if drawing exists //
            if (new Repositories.CTrac().DrawingExists(drawing) == true)
            {
                return drawing;
            }
            else
            {
                return string.Empty;
            }
        }

        
    }
}
