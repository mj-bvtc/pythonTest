using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Rhino;

namespace BVTC.RhinoTools.Helpers
{
    public class RhinoAppExt
    {
        /*
        /// <summary>
        /// Pass in prefix, suffix and parametes to write to rhino command line.
        /// </summary>
        /// <param name="prefix"></param>
        /// <param name="suffix"></param>
        /// <param name="args"></param>
        public static void WriteLine(string prefix, string suffix, params<object>[] args)
        {
            string format = prefix;
            List<string> list = new List<string>();
            for (int i = 0; i < args.Length; i++)
            {
                list.Add("{" + i.ToString() + "}");
            }
            format += string.Join(", ", list);
            format += suffix;

            RhinoApp.WriteLine(string.Format(format, args));
        }
        
        /// <summary>
        /// Pass in a prefix and any number of parameters to write to rhino command line.
        /// </summary>
        /// <param name="prefix"></param>
        /// <param name="args"></param>
        public static void WriteLine(string prefix, params[] args)
        {
            WriteLine(prefix, "", args);
        }
        /// <summary>
        /// Pass in any number of parameters and print as a formatted string.
        /// </summary>
        /// <param name="args"></param>
        public static void WriteLine(params[] args)
        {
            WriteLine("", "", args);
        }
        */
    }
}
