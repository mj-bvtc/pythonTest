using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace MethodTester
{

    public class Files
    {
        public string extension { get; set; }
        public string root { get; set; }
        public string filename { get; set; }
        public string fullpath { get; set; }
        public string file { get; set; }
        public bool isExists { get; set; }
        

        public Files(string inputPath)
        {
            extension = Path.GetExtension(inputPath);
            filename = Path.GetFileNameWithoutExtension(inputPath);
            file = Path.GetFileName(inputPath);                             //contains .extension
            root = Path.GetDirectoryName(inputPath);
            fullpath = inputPath;
            isExists = testIfSaved(inputPath);


        }

        public static bool testIfSaved(string testFile)
        {
            //set a boolean
            bool saveStatus = false;



            //test if there is a value or not
            if (string.IsNullOrEmpty(testFile))
            {
                saveStatus = false;
            }
            else
            {
                saveStatus = true;
            }

            //return result
            return saveStatus;
        }
        public string GetSaveAs(string oldfile, bool addTimeStamp, params object[] SuffixesToAppend)
        {

            Files file = new Files(oldfile);
            string timestamp = GetTimeStamp(DateTime.Now);

            string suffix = string.Join("_", SuffixesToAppend);
            if (addTimeStamp) { suffix += "_" + timestamp; }


            if (string.IsNullOrEmpty(suffix))
            {
                return oldfile;
            }
            else
            {
                string newpath = file.root + "\\" + suffix + file.extension;
                return newpath;
            }


        }
        public static string GetTimeStamp(DateTime value)
        {
            return value.ToString("yyyyMMddHHmmss");
        }
        public static bool checkExtension(string fileToTest, string extensionToLookFor)
        {
            Files file = new Files(fileToTest);
            if (file.extension.ToUpper() == extensionToLookFor.ToUpper())
            {
                return true;
            }
            else
            {
                return false;
            }
        }

    }
}
