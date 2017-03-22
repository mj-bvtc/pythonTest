using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.ConsoleApps
{
    public static class ctracFunctions
    {
        public static void FindLockedFiles(string folder, string ext)
        {
            System.IO.DirectoryInfo dir = new System.IO.DirectoryInfo(folder);
            foreach (System.IO.FileInfo file in dir.GetFiles())
            {
                if (file.Extension.ToUpper() == ext)
                {
                    if (BVTC.osTools.FileTools.IsFileLocked(file) == true)
                    {
                        Console.WriteLine("{0} is locked.", file.FullName);
                    }
                }
            }
        }
        

    }
}
