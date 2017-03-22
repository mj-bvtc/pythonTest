using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Helpers
{
    public static class ObjectExtensions
    {
        public static string PervasiveFormat(this object obj, Type type)
        {
            string value = "";
            // add quotes to all strings //
            if (type == typeof(string))
            {
                value = "'" + (string)obj + "'";
            }
            // convert bool to 0 or 1 //
            else if (type == typeof(bool))
            {
                if ((bool)obj == true)
                    value = "1";
                else
                    value = "0";
            }
            // convert DateTime to 'YYYYmmDD' //
            else if (type == typeof(DateTime))
            {
                DateTime dt = (DateTime)obj;
                value = "'" + dt.ToString("yyyyMMdd", System.Globalization.CultureInfo.GetCultureInfo("en-US")) + "'";
            }
            // convert intergers to string w/o quotes //
            else if (type == typeof(int))
            {
                int i = (int)obj;
                value = i.ToString();
            }
            // convert double floating point number to string w/o quotes //
            else if (type == typeof(double))
            {
                double d = (double)obj;
                value = d.ToString();
            }
            // convert single floating point number to string w/o quotes //
            else if (type == typeof(System.Single))
            {
                Single d = (Single)obj;
                value = d.ToString();
            }
            else if (type == typeof(System.DBNull))
            {
                // add an empty string //
                value = "'" + string.Empty + "'";
            }
            else
            {

                throw new Exception(string.Format("no method to handle {0}", type));
            }



            return value;
        }
    }
}
