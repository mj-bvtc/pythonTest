using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.RhinoTools.Helpers
{
    public static class Double_Extensions
    {
        public static string ToFraction(this double number, int percision, string suffix)
        {
            // create string to store result in //
            string result = "";

            // get leading integer and add to result if not zero //
            int wholeInt = (int)number;
            if (wholeInt != 0)
            {
                result += wholeInt.ToString();
            }

            // get decimal value after subtracting whole number //
            double dec = number - wholeInt;
            int upper = (int)Math.Round(dec * percision, 0);

            // if the denominator is greater than one try to reduce the fraction //
            int[] fraction = new int[] { upper, percision };
            if (upper != 0)
            {
                // add the dash between whole and fractional numbers //
                if (wholeInt > 0)
                {
                    result += "-";
                }
                // loop through all possible reductions for fractions //
                for (int i = 2; i <= percision; i++)
                {
                    if (upper % i == 0 && percision % i == 0)
                    {
                        fraction[0] = upper / i;
                        fraction[1] = percision / i;
                    }
                }
                // if fraction reduces to 1/1 round the number up //
                if (fraction[0] == 1 && fraction[1] == 1)
                {
                    result = (wholeInt + 1).ToString();
                }
                // create fraction string //
                else
                {
                    result += fraction[0].ToString() + "/" + fraction[1].ToString();
                }

            }
            // add suffix for inches onto non-zero values //
            if (result != "")
            {
                result += suffix;
            }


            Console.WriteLine(string.Format("{0} => {1}", number, result));
            return result;

        }
        public static string ToFraction(this double number)
        {
            return ToFraction(number, 16, '"'.ToString());
        }
    }
}
