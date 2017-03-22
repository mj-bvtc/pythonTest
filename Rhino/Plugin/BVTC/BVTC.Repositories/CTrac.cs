using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;

using Pervasive.Data.SqlClient;

using BVTC.Repositories.Helpers;

namespace BVTC.Repositories
{
    public class CTrac : Pervasive
    {
        public CTrac() : base("10.100.100.6", "CTrac1")
        {
            // this will create a connection to C-Trac using standard a method //
        }

        public bool DrawingExists(string drawing, string projNumber)
        {
            bool exists = false;

            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }

            // return false if no drawing was specified //
            if (string.IsNullOrEmpty(drawing) == true) { return exists; }

            // build command string //
            string sqlCmd = string.Format("SELECT DrawingExists('{0}', '{1}')", projNumber, drawing);
            int r = 0;
            try
            {
                // run command and parse into integer //
                int.TryParse(this.CommandToString(sqlCmd), out r);
            }
            finally
            {
                // always close connection //
                this.CloseDB();
            }

            // retun results //
            if (r > 0) { return true; }
            return exists;
        }
        public bool DrawingExists(string drawing)
        {
            return DrawingExists(drawing, "");
        }
        
        public void DeleteSubmittal(string projectNumber, int submittal)
        {
            if (this.setup == false) { this.OpenDB(); }
            try
            {
                this.ExecuteCommand(string.Format(
                    "CALL Delete_Submittal('{0}', {1})", projectNumber, submittal));
            }
            finally { this.CloseDB(); }
        }

        public string Get_Drawing(Guid guid)
        {
            string drawing = "";
            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("SELECT DrawingFromGUID('{0}')", guid.ToString());
            try
            {

                drawing = this.CommandToString(sqlCmd);
            }
            // not currently trying to catch or handle exceptions here //
            finally
            {
                this.CloseDB();
            }

            return drawing;
        }

        public DataTable Get_Drawings(string projectNumber)
        {
            System.Data.DataTable dt = new System.Data.DataTable();

            // if a blank project is input return a blank table //
            if (string.IsNullOrEmpty(projectNumber)) { return dt; }

            // make sure database is open //
            if (this.setup == false) { this.OpenDB(); }

            // execute sql command and close DB //
            string sqlCmd = string.Format("CALL Get_Drawings('{0}')", projectNumber);
            try { dt = this.CommandToDataTable(sqlCmd); }
            finally { this.CloseDB(); }

            return dt;
        }

        public string Get_CurrentUser()
        {
            string user = string.Empty;
            if (this.setup == false) { this.OpenDB(); }

            try
            {
                // pull user initial from C-Trac list //
                user = this.CommandToString(
                    string.Format("SELECT Get_User('{0}')", Environment.UserName));
            }
            finally
            {
                this.CloseDB();
            }

            return user;
        }

        public DataTable Get_MoldShopComments(string drawing, string projectNum)
        {
            System.Data.DataTable dt = new System.Data.DataTable();

            if (this.setup == false) { this.OpenDB(); }


            string sqlCmd = string.Format("Call Get_MoldComments('{0}', '{1}')", projectNum, drawing);

            try
            {
                dt = this.CommandToDataTable(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }

            return dt;
        }

        public List<string> Get_LayerNames(string englishName, string layout)
        {
            List<string> layers = new List<string>();

            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("Call Get_TextLayers('{0}', '{1}')", englishName, layout);

            try
            {
                layers = this.CommandToList(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }


            return layers;
        }

        public int CountSubmittals(string projectNumber)
        {
            int submittal = -1;

            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("SELECT CountSubmittals('{0}')", projectNumber);

            try
            {
                string result = this.CommandToString(sqlCmd);
                Int32.TryParse(result, out submittal);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }


            return submittal;
        }
        public List<string> SubmittalList(string projectNumber)
        {
            List<string> submittals = new List<string>();
            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("CALL SubmittalList('{0}')", projectNumber);

            try
            {
                submittals = this.CommandToList(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }


            return submittals;
        }

        public DataTable Get_PdfList(string projectNumber)
        {
            System.Data.DataTable dt = new System.Data.DataTable();
            if (this.setup == false) { this.OpenDB(); }
            string sqlCmd = string.Format("Call Get_PDF_List('{0}')", projectNumber);
            try
            {
                dt = this.CommandToDataTable(sqlCmd);
                if (dt.Rows.Count == 0)
                {
                    throw new Exceptions.DataMissing(string.Format(
                        "Could not find any drawings in C-Trac for project: '{0}'", projectNumber));
                }
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }

            return dt;
        }

        public List<string> Get_Projects()
        {
            List<string> projects = new List<string>();

            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = "Call Get_Projects()";

            try
            {
                projects = this.CommandToList(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }


            return projects;
        }

        public string Get_ProjectName(string projectNumber)
        {
            string shortDescription = "";
            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }
            // return false if no drawing was specified //
            if (string.IsNullOrEmpty(projectNumber) == true) { return shortDescription; }
            // create command string //
            string sqlCmd = string.Format("SELECT Find_ProjectName('{0}')", projectNumber);
            // execute command or throw error //
            try
            {
                shortDescription = this.CommandToString(sqlCmd);
            }
            finally
            {
                this.CloseDB();
            }

            return shortDescription;
        }

        public string Get_ProjectNumber(string shortDescription)
        {
            string projectNumber = string.Empty;

            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }

            // return false if no drawing was specified //
            if (string.IsNullOrEmpty(shortDescription) == true) { return projectNumber; }

            string sqlCmd = string.Format("SELECT Find_ProjectNumber('{0}')", shortDescription);

            try
            {
                projectNumber = this.CommandToString(sqlCmd);
            }
            finally
            {
                this.CloseDB();
            }

            return projectNumber;
        }
        public string Get_ProjectNumber(Guid id)
        {
            string projectNumber = string.Empty;
            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }
            // return false if no drawing was specified //

            string sqlCmd = string.Format("SELECT {0} FROM {1} WHERE {2} = '{3}'",
                '"' + "Project Number" + '"', "DraftingData", "Guid", id );
            try
            {
                projectNumber = this.CommandToString(sqlCmd);
            }
            finally
            {
                this.CloseDB();
            }

            return projectNumber;
        }

        public string Get_Pcode(string projectNumber)
        {
            string pCode = string.Empty;

            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }

            // return false if no drawing was specified //
            if (string.IsNullOrEmpty(projectNumber) == true) { return projectNumber; }
            string sqlCmd = string.Format("SELECT Find_Pcode('{0}')", projectNumber);

            try
            {
                pCode = this.CommandToString(sqlCmd);
            }
            finally
            {
                this.CloseDB();
            }

            return pCode;
        }

        public DataTable Get_Revisions(Guid id)
        {
            System.Data.DataTable dt = new System.Data.DataTable();

            if (this.setup == false) { this.OpenDB(); }
            try
            {
                dt = this.CommandToDataTable(
                    string.Format("CALL Get_Revision('{0}')", id));
            }
            finally { this.CloseDB(); }

            return dt;
        }

        public string Get_RevisionLetter(Guid id)
        {
            string revLetter = "";
            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("SELECT RevisionLetter('{0}')", id);
            try
            {
                revLetter = this.CommandToString(sqlCmd);
            }
            finally { this.CloseDB(); }

            return revLetter;
        }

        public List<string> Get_ShortDescriptions()
        {
            List<string> pNames = new List<string>();

            // make sure connection is open //
            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("SELECT {0} FROM {1}", '"' + "Short Description" + '"', '"' + "Project Master Heade" + '"');
            try
            {
                pNames = this.CommandToList(sqlCmd);
            }
            finally { this.CloseDB(); }

            return pNames;
        }

        /// <summary>
        /// Query CTrac1.RhinoLocations to find all rows of data location information for
        /// the placing Rhino text objects on a document.  
        /// </summary>
        /// <param name="englishName"></param>
        /// <param name="pageName"></param>
        /// <returns>DataTable containing all rows for input parameters</returns>
        public DataTable Get_TextInformation(string englishName, string pageName)
        {
            System.Data.DataTable dt = new System.Data.DataTable();

            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("CALL Get_TextLocations('{0}','{1}')", englishName, pageName);

            try
            {
                // text layout info from C-Trac into DataTable //
                dt = this.CommandToDataTable(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }

            return dt;
        }
        public DataTable Get_TextInformation(string englishName, string pageName, string ctField)
        {
            System.Data.DataTable dt = new System.Data.DataTable();

            if (this.setup == false) { this.OpenDB(); }

            string sqlCmd = string.Format("CALL Get_TextLocation('{0}','{1}','{2}')", englishName, pageName, ctField);

            try
            {
                // text layout info from C-Trac into DataTable //
                dt = this.CommandToDataTable(sqlCmd);
            }
            finally
            {
                // always close the database //
                this.CloseDB();
            }

            return dt;
        }
        public DataTable Get_TextInformation(string englishName, string pageName, List<string> headings)
        {
            System.Data.DataTable dt = new System.Data.DataTable();
            for (int i = 0; i < headings.Count; i++)
            {
                if (i == 0)
                {
                    dt = Get_TextInformation(englishName, pageName, headings[i]);
                }
                else
                {
                    System.Data.DataTable addtl = Get_TextInformation(englishName, pageName, headings[i]);
                    if (addtl.Rows.Count > 0)
                    {
                        dt.ImportRow(addtl.Rows[0]);
                    }
                }
            }
            return dt;
        }

        public void Insert_Weight(double estBatch, double estFired, double estShip, 
            double actBatch, double actFired, double actShip, string path)
        {
            if (this.setup == false) { this.OpenDB(); }

            try
            {
                string cmd = string.Format("CALL Insert_Weights({0},{1},{2},{3},{4},{5},'{6}')",
                    estBatch, estFired, estShip, actBatch, actFired, actShip, path);
                this.ExecuteCommand(cmd);
            }
            finally
            { this.CloseDB(); }
        }

        public int Update_ClientPDF(Guid id, string path)
        {
            int recordsAffected = 0;

            // create update string //
            string sqlCmd = string.Format("CALL Update_ClientPDF('{0}', '{1}')", id, path);

            // setup connection //
            if (this.setup == false) { this.OpenDB(); }
            // execute update command //
            try { recordsAffected += this.ExecuteCommand(sqlCmd); }
            // catch errors //
            finally { this.CloseDB(); }

            return recordsAffected;
        }
        public int Update_ShopPDF(Guid id, string path)
        {
            int recordsAffected = 0;

            // create update string //
            string sqlCmd = string.Format("CALL Update_ShopPDF('{0}', '{1}')", id, path);

            // setup connection //
            if (this.setup == false) { this.OpenDB(); }
            // execute update command //
            try { recordsAffected += this.ExecuteCommand(sqlCmd); }
            // catch errors //
            finally { this.CloseDB(); }

            return recordsAffected;
        }

        public int Update_MoldShopComments(System.Data.DataTable comments, string projectNumber, string[] headings)
        {
            int recordAffected = 0;

            List<string> colList = comments.GetHeadings(true);
            foreach (DataRow row in comments.Rows)
            {
                // Create string list of values to be joined in sql command //
                List<string> list = new List<string>() { string.Format("'{0}'", projectNumber) };

                foreach (string propName in headings)
                {
                    if (colList.Contains(propName))
                    {
                        int index = colList.IndexOf(propName);
                        list.Add(row[index].PervasiveFormat(row[index].GetType()));
                    }
                }
                // generate command //
                string sqlCmd = "CALL Update_MoldComments(" + string.Join(", ", list) + ")";

                // setup connection //
                if (this.setup == false) { this.OpenDB(); }

                // execute update command //
                try { recordAffected += this.ExecuteCommand(sqlCmd); }

                // catch errors //
                finally { this.CloseDB(); }
            }

            return recordAffected;

        }
        public int Update_MoldShopComments(System.Data.DataTable comments, string projectNumber)
        {
            string[] headings = new string[]
            {
                "Block ID",
                "Left",
                "Right",
                "Top",
                "Bottom",
                "Rear",
                "Front",
                "Use Mold",
                "Mold Type",
                "Qty Molds",
                "Comments",
                "Pressing Comments",
                "Finishing Comments"
            };

            // run with default list of headings //
            return Update_MoldShopComments(comments, projectNumber, headings);
        }

        public void Update_RevisionStamp(System.Data.DataTable dt, Guid id)
        {
            if (this.setup == false) { this.OpenDB(); }

            try
            {
                foreach (DataRow row in dt.Rows)
                {
                    this.ExecuteCommand(string.Format(
                        "CALL Upsert_Revision('{0}', '{1}', '{2}', '{3}', '{4}')",
                        id, row[0], row[1], row[2], row[3]));
                }
            }
            finally
            { this.CloseDB(); }

        }

        public void Call(string storedProcedure, params object[] variables) //formats a call to ctrac
        {

            OpenDB();
            /*

            ///Example///
            string pNum = "P14-0509";
            string pName = "Woolworth";
            string part = "3b_1";
            string useMold = "3b";

            string call = OtherClass.Call("InsertStockData2", pNum, pName, part, useMold);
            Console.WriteLine(call);
            Console.ReadLine();

            result: Call InsertStockData2('P14-0509','Woolworth','3b_1','3b')
            */

            //string result = "Call " +storedProcedure+"("; //beginning of command  //first working option
            string result = string.Format("Call {0}(", storedProcedure); //beginning of command, formats in stored procedure
            string format = "'{0}',"; //base case for each variable in list
            foreach (var v in variables)
            {
                string res = string.Format(format, v);
                result += res;
            }
            string newString = result.Remove(result.Length - 1); //remove uneccessary last comma
            newString += ")"; }//end parenthesis

        public string Upsert_SubmittalDetail(Guid id, int submitNumber, string submitTo)
        {
            if (this.setup == false) { this.OpenDB(); }
            string cmd = string.Format("CALL Upsert_SubmittalDetail('{0}','{2}',{1})", id, submitNumber, submitTo);
            try { this.ExecuteCommand(cmd); }
            finally { this.CloseDB(); }
            return cmd;
        }
        public string Upsert_SubmittalHeader(string projectNumber, int submitNumber, string submitTo)
        {
            if (this.setup == false) { this.OpenDB(); }
            string cmd = string.Format("CALL Upsert_SubmittalHeader('{0}','{2}',{1})", projectNumber, submitNumber, submitTo);
            try { this.ExecuteCommand(cmd); }
            finally { this.CloseDB(); }
            return cmd;
        }
            ///////////////////////////////////////////////error here, will not update, commenting out for compiling 3.7.2017//////////////////////
            //ctrac.CommandToDataTable(newString);
            //string cmdStr2 = newString;
            //RhinoApp.WriteLine(cmdStr);

            // run update command //
            //PsqlCommand updateCmd = new PsqlCommand(cmd, conn);
            //int r = updateCmd.ExecuteNonQuery();

            // Write Results in Console Window //
            //RhinoApp.WriteLine(r.ToString() + " Row(s) Effected");
            //CTrac.CloseDB();

        } 

    }

