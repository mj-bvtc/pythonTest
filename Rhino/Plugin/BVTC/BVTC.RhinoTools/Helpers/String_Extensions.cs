using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.RhinoTools.Helpers
{
    public static class String_Extensions
    {
        public static string StripExtension(this string str)
        {
            if (str.Contains("."))
            {
                return str.Substring(0, str.LastIndexOf("."));
            }

            return str;
        }
    }
}
