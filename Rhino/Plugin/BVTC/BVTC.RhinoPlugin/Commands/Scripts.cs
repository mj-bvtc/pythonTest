using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Rhino;
using Rhino.Commands;

namespace BVTC.RhinoPlugin.Commands
{
    class Scripts
    {
        public static Result GetProjectName(BVTC.Data.Stock.StockData sd, Rhino.RhinoDoc doc)
        {
            //get pnum and pname
            string pname = RhinoTools.FileStructure.Find_ProjectName(doc);          //try to find pname through file structure


            //check if pname empty
            if (string.IsNullOrEmpty(pname))
            {
                UI.ProjectBrowser projectBrowser = new UI.ProjectBrowser(sd);       //use browser to locate pname
                var pbresult = Rhino.UI.Dialogs.ShowSemiModal(projectBrowser);      //this is the result of form showing up
                if (pbresult == System.Windows.Forms.DialogResult.OK)
                {
                    RhinoApp.WriteLine("Got pnum and pname!");
                    sd.ProjectName = projectBrowser.dd.ProjectName;
                    sd.ProjectNumber = projectBrowser.dd.ProjectNumber;
                }
                else { return Result.Cancel; }                                      //cancel if that does not work

            }
            else
            {
                // if function finds result, check if pname is valid
                BVTC.Repositories.CTrac CTrac = new Repositories.CTrac();


                //list of current projects
                string cmd = "Call Get_Projects()";
                List<string> projects = CTrac.CommandToList(cmd);

                bool isValid = projects.Contains(pname);
                if (isValid)
                {
                    //RhinoApp.WriteLine(pname);
                    RhinoApp.WriteLine("This project exists in CTrac");
                    sd.ProjectName = pname;
                }
                else
                {
                    //RhinoApp.WriteLine(pname);
                    RhinoApp.WriteLine("No projects match in CTrac");
                    return Result.Cancel;                                           //cancel due to bad project
                }

                
            }
            return Result.Success;
        }

        public static Result ExportBlocks(List<Guid> blockIds, string file)
        {
            string cmd = "-_Export ";
            foreach (var id in blockIds)
            {
                cmd += "_SelID ";
                cmd += id.ToString();
            }
            cmd += "_Enter ";
            cmd += "_Enter ";
            cmd += '"' + file + '"' + ' ';

            bool success = RhinoApp.RunScript(cmd, false);
            if (success) { RhinoApp.WriteLine(string.Format("Export to {0} worked!", file)); }



            return Result.Success;

        }
    }
}
