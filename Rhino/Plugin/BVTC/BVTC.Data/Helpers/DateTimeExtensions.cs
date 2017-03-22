using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data.Helpers
{
    public static class DateTimeExtensions
    {
        // extension methods for DateTime //
        public static string CTracFormat(this DateTime date)
        {
            return date.ToString("yyyyMMdd", System.Globalization.CultureInfo.GetCultureInfo("en-US"));
        }
    }
}
