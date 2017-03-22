using System;
using System.Collections.Generic;

using System.Windows.Forms;
using Pervasive.Data.SqlClient;
using System.Text.RegularExpressions;
using System.CodeDom.Compiler;
using System.CodeDom;
using System.IO;
using System.Data;
using System.Reflection;
using System.Linq;
using System.Linq.Expressions;


namespace BVTC.Application.Test
{
    class Program
    {
        static void Main(string[] args)
        {
            Ctrac ctrac = new Ctrac();
            ctrac.SetupDB();

            //List<string> projects = ctrac.AllProjects();
            //foreach (var pro in projects)
            //{
            //    Console.WriteLine(pro);
            //}

            //string cmd = "CALL\"Get_Projects\"()";
            //List<string> projects = ctrac.CommandToList(cmd);
            
            /*
            foreach (var pro in projects)
            {
                Console.WriteLine(pro);
            }
            
            Console.WriteLine("Type in a project to test: ");
            string project = Console.ReadLine();
            bool answer = ctrac.verifyProject(project);
            Console.WriteLine(answer.ToString());

            */



            Console.ReadLine();
            ctrac.CloseDB();

        }
            public class Ctrac
        {
            public bool setup { get; set; }
            public PsqlConnection conn { get; set; }

            public void SetupDB()
            {

                // Make sure the computer has access to the .SDF file.
                // Setup and open() the connection to the SDF database. 

                this.setup = false;
                // Make Connection string for CTRAC1 //
                string conn_str = "Server Name=10.100.100.6;Database Name=CTRAC1;";

                try
                {
                    // try to create new connection and open it //
                    this.conn = new PsqlConnection(conn_str);
                    this.conn.Open();
                    this.setup = true;
                }
                catch
                {
                    // if something goes wrong: setup to false //
                    this.setup = false;
                }
            }

            public List<string> ProgramsNeeded()
            {
                // Return all completed stocks with no toolpath //

                List<string> modelPaths = new List<string>();

                if (this.setup == false) { return modelPaths; }

                // Create SQL Command //
                string cmdStr = "CALL ProgramsNeeded()";
                DataTable dt = this.CommandToDataTable(cmdStr);

                // Loop through DataTable //
                foreach (DataRow row in dt.Rows)
                {
                    // add model paths to list of paths //
                    modelPaths.Add(row[0].ToString().Trim());
                }
                return modelPaths;
            }

            public List<string> ModelsMadeByProject(string projNum)
            {
                // create empty List //
                List<string> moldList = new List<string>();
                if (this.setup == false) { return moldList; }

                // create SQL command string //
                string cmdStr = "CALL MoldsMadeByProject('" + projNum + "')";

                DataTable dt = this.CommandToDataTable(cmdStr);

                // Loop through DataTable for molds //
                foreach (DataRow row in dt.Rows)
                {
                    moldList.Add(row[0].ToString().Trim());
                }
                return moldList;
            }

            public List<string> UseMold_ByProject(string projNum)
            {
                List<string> moldList = new List<string>();

                if (this.setup == false) { return moldList; }

                // Create SQL Command //
                string cmdStr = "CALL Distinct_UseMold('" + projNum + "')";
                DataTable dt = this.CommandToDataTable(cmdStr);

                // Loop through DataTable //
                foreach (DataRow row in dt.Rows)
                {
                    // add model paths to list of paths //
                    moldList.Add(row[0].ToString().Trim());
                }
                return moldList;
            }

            public void Update_UseMold(string projNum, string mold)
            {
                if (this.setup == false) { return; }

                // Create update SQL command //
                string cmdStr = "CALL Update_UseMold('" + projNum + "', '" + mold + "')";
                Console.WriteLine(cmdStr);
                // run update command //
                PsqlCommand updateCmd = new PsqlCommand(cmdStr, this.conn);
                int r = updateCmd.ExecuteNonQuery();

                // Write Results in Console Window //
                Console.WriteLine(r.ToString() + " Row(s) Effected");

            }

            public void AutoFillModel(string projNum, string useMold)
            {
                if (this.setup == false) { return; }

                // create SQL command string //
                string cmdStr = "CALL AutoFillModel('" + projNum + "', '" + useMold + "')";
                Console.WriteLine(cmdStr);

                // run update command //
                PsqlCommand updateCmd = new PsqlCommand(cmdStr, this.conn);
                int r = updateCmd.ExecuteNonQuery();

                // Write Results in Console Window //
                Console.WriteLine(r.ToString() + " Row(s) Effected");
            }

            public DataTable StatusTable()
            {
                // create SQL command string //
                string cmdStr = "CALL MoldStatus()";
                return CommandToDataTable(cmdStr);
            }

            public DataTable ProjNumName()
            {
                // create SQL command string //
                string cmdStr = "Call Get_PnumPname()";
                return CommandToDataTable(cmdStr);
            }

            public DataTable CommandToDataTable(string cmdStr)
            {
                // create new DataTable //
                DataTable dt = new DataTable();
                if (this.setup == false) { return dt; }

                try
                {
                    PsqlCommand cmd = new PsqlCommand(cmdStr, this.conn);

                    // load and close reader //
                    PsqlDataReader reader = cmd.ExecuteReader();
                    dt.Load(reader);
                    reader.Close();
                }
                catch { Console.WriteLine("Could not execute command: " + cmdStr); }
                return dt;
            }

            public List<string> CommandToList(string cmdStr)
            {
                // create new DataTable //
                List<string> list = new List<string>();
                if (this.setup == false) { return list; }

                try
                {
                    PsqlCommand cmd = new PsqlCommand(cmdStr, this.conn);

                    // load and close reader //
                    PsqlDataReader reader = cmd.ExecuteReader();
                    while (reader.Read())
                    {
                        var value = reader[0];
                        string str;
                        // trim white space from behind CHAR() data //
                        if (value.GetType() == typeof(string))
                            str = ((string)value).Trim();
                        // convert non-strings to strings //
                        else
                            str = value.ToString();
                        // add resulting string to list //
                        list.Add(str);

                    }
                    reader.Close();
                }
                catch { }//Console.WriteLine("Could not execute command: " + cmdStr); }
                return list;
            }

            public string CommandToString(string cmdStr)
            {
                //SetupDB();
                string result = "";
                // create new DataTable //
                DataTable dt = new DataTable();
                if (this.setup == false) { return result; }

                try
                {
                    PsqlCommand cmd = new PsqlCommand(cmdStr, this.conn);

                    // load and close reader //
                    PsqlDataReader reader = cmd.ExecuteReader();
                    reader.Read();
                    result = reader.GetString(0);

                    reader.Close();
                }
                catch { Console.WriteLine("Could not execute command: " + cmdStr); }
                //CloseDB();
                return result;
            }

            public int ExecuteCommand(string cmdStr)
            {
                /* Executes a non-query PSQL command.
                 * Used for deletes, inserts or updates.
                 * Will return the number of rows effected.
                 * -1 signifies an error processing the command.
                 */
                int result = 0;
                if (this.setup == false) { return result; }
                try
                {
                    PsqlCommand cmd = new PsqlCommand(cmdStr, this.conn);
                    // run command //
                    result = cmd.ExecuteNonQuery();
                }
                catch
                {
                    Console.WriteLine("Could not execute command: " + cmdStr);
                    return -1;
                }

                // result is the number of rows effected //
                return result;
            }

            public string getPname(string pNum)
            {

                string cmdStr = "CALL Get_Pname('" + pNum + "' )";
                string result = CommandToString(cmdStr);
                return result;
            }

            public void CloseDB()
            {
                //Close the connection.
                //Very important so we don't leave open threads/seats on DB.
                try { this.conn.Close(); }
                catch { Console.WriteLine("this.connection could not be closed"); }
                finally { this.setup = false; }
            }

            public void Insert_StockTable(string pNum, string pName, string part)
            {
                this.SetupDB();
                if (this.setup == false) { return; }

                // Create update SQL command //
                string cmd = "CALL InsertStockData2('{0}','{1}','{2}')";
                string cmdStr = string.Format(cmd, pNum, pName, part);
                Console.WriteLine(cmdStr);
                // run update command //
                PsqlCommand updateCmd = new PsqlCommand(cmdStr, this.conn);
                int r = updateCmd.ExecuteNonQuery();

                // Write Results in Console Window //
                Console.WriteLine(r.ToString() + " Row(s) Effected");
                this.CloseDB();
            }

            public void Insert_StockTable(
                string part,
                string pNum,
                string useMold,
                string method,
                int stockLen,
                int stockWidth,
                int stockHeight,
                string stockDate,
                string pgmDate,
                string verifyDate,
                int emt,
                string partStartDate,
                int partStartTime,
                string partEndDate,
                int partEndTime,
                int partRun,
                string partCompleteDate,
                string modelPath,
                string guid,
                string notUsed,
                int stockCut,
                int wireCutTrad,
                double shrinkage
                )
            {
                this.SetupDB();
                if (this.setup == false) { return; }

                // Create update SQL command //
                string cmd = "CALL InsertStockData('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}')";
                string cmdStr = string.Format(
                    cmd,
                    part,
                    pNum,
                    useMold,
                    method,
                    stockLen,
                    stockWidth,
                    stockHeight,
                    stockDate,
                    pgmDate,
                    verifyDate,
                    emt,
                    partStartDate,
                    partStartTime,
                    partEndDate,
                    partEndTime,
                    partRun,
                    partCompleteDate,
                    modelPath,
                    guid,
                    notUsed,
                    stockCut,
                    wireCutTrad,
                    shrinkage
                    );
                Console.WriteLine(cmdStr);
                // run update command //
                PsqlCommand updateCmd = new PsqlCommand(cmdStr, this.conn);
                int r = updateCmd.ExecuteNonQuery();

                // Write Results in Console Window //
                Console.WriteLine(r.ToString() + " Row(s) Effected");
                this.CloseDB();
            }


            public bool IsProjectNameValid(string Pname)
            {
                bool result = false;
                Ctrac ctrac = new Ctrac();
                ctrac.SetupDB();
                string cmd = "select \"Short Description\" from \"Project Master Heade\"";
                List<string> projects = ctrac.CommandToList(cmd);
                foreach (var project in projects)
                {
                    //Console.WriteLine(project);
                    if (Pname.ToUpper() == project.ToUpper())
                    {
                        result = true;
                        Console.WriteLine("Match found!");
                    }
                    else
                    {

                    }
                }

                ctrac.CloseDB();
                return result;
            }

            public List<string> updateUseMold(string cmdStr)
            {
                string s1 = "CALL Distinct_UseMold('";
                string s2 = "')";
                string newCmd = s1 + cmdStr + s2;

                SetupDB();
                List<string> moldList = CommandToList(newCmd);
                CloseDB();
                return moldList;
            }
            public void addMoldsToCombo(ComboBox combobox1, List<string> moldList)
            {
                foreach (string mold in moldList)
                {
                    combobox1.Items.Add(mold);
                }
            }
            public void addDrawingsToListbox(List<string> drawingList, ListBox listbox)
            {
                listbox.Items.Clear();
                foreach (string dwg in drawingList)
                {
                    listbox.Items.Add(dwg);
                }
            }
            public List<string> drawingList(string pnumber, string usemold)
            {
                string s1 = "CALL Drawings_By_Mold('";
                string s2 = "')";
                string newCmd = s1 + pnumber + "','" + usemold + s2;

                SetupDB();
                List<string> drawinglist = CommandToList(newCmd);
                CloseDB();
                return drawinglist;
            }
            public void updateQuantity(string pnumber, string usemold, TextBox quantity)
            {
                string s1 = "CALL Sum_UseMold('";
                string s2 = "')";
                string newCmd = s1 + pnumber + "','" + usemold + s2;
                SetupDB();
                DataTable dt = CommandToDataTable(newCmd);
                CloseDB();
                quantity.Text = dt.Rows[0][0].ToString();
            }
            /// <summary>
            /// Takes in a string with bad characters and removes them
            /// </summary>
            public string cleanString(string input)
            {
                string literal = "";
                using (var writer = new StringWriter())
                {
                    using (var provider = CodeDomProvider.CreateProvider("CSharp"))
                    {
                        provider.GenerateCodeFromExpression(new CodePrimitiveExpression(input), writer, null);
                        literal = writer.ToString();
                    }
                }
                Regex re = new Regex("[;\\\\/:*?\"<>|']");
                string outputString = re.Replace(literal, "");
                return outputString;
            }
            public string correctStringOneAnd(string input)
            {
                string result = input;
                if (input.Contains("&&"))
                {
                    string newStr = input.Replace("&&", "&");
                    result = newStr;
                }
                result = cleanString(result);
                return result;
            }
            public string correctStringTwoAnds(string input)
            {
                string result = input;
                if (input.Contains("/"))
                {
                    string newStr = input.Replace("/", "&&");
                    result = newStr;
                }
                if (input.Contains(@"\"))
                {
                    string newStr = input.Replace(@"\", "&&");
                    result = newStr;
                }
                result = cleanString(result);
                return result;
            }
            public static string getData(object obj)
            {
                //gets data and prints field name and value to console window
                FieldInfo[] fields = obj.GetType().GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                System.String str = "";
                foreach (FieldInfo f in fields)
                {
                    str += f.Name + " = " + f.GetValue(obj) + "\n";
                }
                string str2 = str.Replace("<", "");
                string str3 = str2.Replace(">k__BackingField", "");
                return str3;
            }
            public static List<Tuple<string, object>> getTupleListData(object obj)
            {
                //gets data and assigns (name, object) to a list of tuples
                List<Tuple<string, object>> listOfTuples = new List<Tuple<string, object>>();
                FieldInfo[] fields = obj.GetType().GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                System.String str = "";
                foreach (FieldInfo f in fields)
                {
                    str += f.Name + " = " + f.GetValue(obj) + "\n";
                    string halfName = f.Name.Replace("<", "");
                    string cleanName = halfName.Replace(">k__BackingField", "");
                    var tupleResult = Tuple.Create(cleanName, f.GetValue(obj));
                    listOfTuples.Add(tupleResult);
                }

                string str2 = str.Replace("<", "");
                string str3 = str2.Replace(">k__BackingField", "");
                //Console.WriteLine(str3);
                //Console.ReadLine();
                return listOfTuples;
            }
            public void Call(string storedProcedure, params object[] variables) //formats a call to ctrac
            {

                SetupDB();
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
                newString += ")"; //end parenthesis

                //ctrac.CommandToDataTable(newString);
                string cmdStr = newString;
                Console.WriteLine(cmdStr);

                // run update command //
                PsqlCommand updateCmd = new PsqlCommand(cmdStr, conn);
                int r = updateCmd.ExecuteNonQuery();

                // Write Results in Console Window //
                Console.WriteLine(r.ToString() + " Row(s) Effected");
                CloseDB();

            }



            public bool verifyProject(string inputProject)
            {
                //tests if project exists in ctrac
                bool result = false;

                //import list of projects from ctrac
                string cmd = "select \"Short Description\" from \"Project Master Heade\"";
                List<string> projects = CommandToList(cmd);

                //test input against list
                foreach (var proj in projects)
                {
                    if (inputProject == proj)
                    {
                        result = true;
                    }
                }

                //return true if it exists



                return result;

            }

            public List<string> AllProjects()
            {
                Ctrac ctrac = new Ctrac();
                ctrac.SetupDB();
                string cmd = "select \"Short Description\" from \"Project Master Heade\"";
                List<string> projects = CommandToList(cmd);
                ctrac.CloseDB();
                return projects;
            }


        }

    }
    
}
