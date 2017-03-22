using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.RhinoTools
{
    class ZoomMode
    {
        enum RunMode
        {
            AutoSize,
            Custom,
            Maximum
        };

        public static string[] ToList()
        {
            string[] modes = Enum.GetValues(typeof(RunMode))
                .Cast<string>()
                .Select(x => x.ToString())
                .ToArray();

            return modes;
        }
    }
}
