using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;

using BVTC;
using BVTC.Data.Helpers;
using BVTC.osTools;



namespace BVTC.ConsoleApps
{
    class Program
    {
        static void Main(string[] args)
        {

            /*
            // get document guid //
            string guid = "10b7948f-8c55-4db6-9245-cc849c181b4c";

            // create data list //
            List<BVTC.Data.Drafting> datalist = new List<BVTC.Data.Drafting>();

            // create connection to C-Trac //
            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
            DataTable dt = new DataTable();
            try
            {
                CTrac.OpenDB();
                dt = CTrac.CommandToDataTable(string.Format("CALL DraftingDataByGUID('{0}')", guid));
            }
            catch (Exception e)
            {
                throw e;
            }
            finally
            {
                CTrac.CloseDB();
            }

            foreach (DataRow row in dt.Rows)
            {
                BVTC.Data.Drafting data = new BVTC.Data.Drafting(row);
                datalist.Add(data);
                data.Quantity = 66;
                data.UpsertCTrac();
            }
            string test = "Quantity";
            Console.WriteLine("'{0}'",test.classFormat());

            ctracFunctions.FindLockedFiles(@"P:\BostValley", ".DAT");
            ctracFunctions.FindLockedFiles(@"P:\BostValley", ".DDF");
            ctracFunctions.FindLockedFiles(@"P:\BostValley\DDFs", ".DDF");
            ctracFunctions.FindLockedFiles(@"P:\BostValley\PS_DDF", ".DDF");
            ctracFunctions.FindLockedFiles(@"P:\BostValley\PS1_DDF", ".DDF");


            //string path = @"V:\Projects\Tester 777\TerraCotta\CS1\P77-7777_CS1.3dm_11x8.5.pdf";
            string path = @"V:\Projects\Tester 777\TerraCotta\CS1\P77-7777_CS1.3dm_17x11.pdf";
            System.IO.FileInfo info = new System.IO.FileInfo(path);
            Console.WriteLine(info.Length);
            */

            string path = @"V:\Projects\Gage Building\TerraCotta";
            System.IO.DirectoryInfo dir = new System.IO.DirectoryInfo(path);
            List<System.IO.FileInfo> files = new List<System.IO.FileInfo>();
            FileTools.WalkDirectoryTree(dir, files, ".pdf");

            foreach (System.IO.FileInfo file in files)
            {
                try
                {
                    PdfTools.RotatePDF(file.FullName);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                }
            }

            Console.WriteLine();
            Console.WriteLine("Press <Enter> to continue:");
            Console.ReadLine();
        }
    }
}
