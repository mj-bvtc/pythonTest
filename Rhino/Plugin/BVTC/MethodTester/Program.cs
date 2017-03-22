using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using BVTC.RhinoTools.Helpers;
using System.IO;

namespace MethodTester
{
    class Program
    {
        static void Main(string[] args)
        {

            string testFile = @"C:\Users\mkreidler\Desktop\Dump\GERBILIA_B2_2_P14-0509_CNC.3DM";
                       

            Files result = new Files(testFile);
            

            Console.WriteLine(Files.testIfSaved(testFile));
            Console.WriteLine(Files.GetTimeStamp(DateTime.Now));
            Console.WriteLine(Files.checkExtension(testFile, ".3dm"));
            Console.WriteLine(result.extension);
            Console.WriteLine(result.isExists);
            Console.WriteLine(result.GetSaveAs(testFile, true, "temp"));
            Console.WriteLine(result.GetSaveAs(testFile, false, "temp", "hamsterecology", "trial2"));
            Console.WriteLine(result.file);
            Console.WriteLine(result.fullpath);

            DirectoryInfo dir = new DirectoryInfo(testFile);


            Console.WriteLine(dir.GetSaveAs(true, "Test"));

            Console.ReadLine();





        }



        


    }
}
