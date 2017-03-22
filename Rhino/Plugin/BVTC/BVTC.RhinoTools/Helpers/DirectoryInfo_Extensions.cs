using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace BVTC.RhinoTools.Helpers
{
    public static class DirectoryInfo_Extensions
    {
        public static string GetSaveAs(this DirectoryInfo info, bool addTimeStamp, params object[] SuffixesToAppend)
        {

            //string fileName = info.Name.Split('.')[0];

            string fileName = "";
            if (addTimeStamp)
            {
                fileName += "\\" + DateTime.Now.ToString("yyyyMMddHHmmss");
            }

            //foreach (var item in SuffixesToAppend)
            //{
            //    fileName += "_" + item.ToString();
            //}

            fileName += string.Join("_", SuffixesToAppend);

            string midPath = info.Parent.FullName + "\\" + fileName + info.Extension;
            string lastPath = midPath.ToUpper().Replace(" ", "");

            return lastPath;
        }

        public static bool verifyExtension(this DirectoryInfo info, string file, string expectedExtension)
        {
            if(info.Extension.ToUpper() == expectedExtension.ToUpper())
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
