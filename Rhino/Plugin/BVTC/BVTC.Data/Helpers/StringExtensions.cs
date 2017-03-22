using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data.Helpers
{
    public static class StringExtensions
    {
        public static string addQuotes(this string str)
        {
            return '"' + str + '"';
        }

        public static string classFormat(this string str)
        {
            return str.Replace(" ", string.Empty).Trim('"');
        }

        public static bool CheckBlockID(this string value)
        {
            bool verified = true;

            if (value != "" && value != null)
            {
                // count dashes //
                int dashCount = (value.Split('-').Length - 1);

                // only allow block id's with a single dash //
                if (dashCount > 1)
                {
                    throw new Exceptions.BlockID_Exception(string.Format(
                        "Block ID invalid: '{0}' may only contain (1) dash.", value));
                }

                // make sure value is only letters and numbers //
                if (value.Replace("-", string.Empty).IsAlphaNum() == false)
                {
                    throw new Exceptions.BlockID_Exception(string.Format(
                        "'{0}' is not a valid Block ID. {1}Block IDs may contain only letters, numbers and a dash", 
                        Environment.NewLine, value));
                }

                // make sure trailing values are only numbers //
                if (dashCount == 1)
                {
                    if (value.Split('-')[1].IsNumber() == false)
                    {
                        throw new Exceptions.BlockID_Exception(string.Format(
                            "{0} is not a valid Block ID.{1}Only numbers may trail the '-'.", value, Environment.NewLine));
                    }
                }
            }
            else
            {
                throw new Exceptions.BlockID_Exception("Block ID value is empty or null.");
            }

            return verified;
        }
        public static bool CheckBlockID(this string value, bool throwExceptions)
        {
            /* Overloaded class method to suppress exceptions if set to true.
             * If a BlockID_Exception is raised false will be returned instead of exception.
             */
            try
            {
                return value.CheckBlockID();
            }
            catch(Exceptions.BlockID_Exception)
            {
                if (throwExceptions == false)
                    return false;
                else
                    throw;
            }
            catch (Exception) { throw; }
        }

        public static string GetBaseStyle(this string value, int maxLength, bool throwException)
        {
            // make sure value is a valid Block ID, with or w/o exceptions //
            if(value.CheckBlockID(throwException) == false) { return string.Empty; }

            // get the string before the '-' //
            string baseStyle = value.Split('-')[0];

            // make sure base style is not more than 5 charectors long //
            if (baseStyle.Length > maxLength)
            {
                if (throwException == true)
                {
                    throw new Exceptions.BlockID_Exception(string.Format(
                        "Block ID '{0}' is more than {1} charectors.", value, maxLength));
                }
                else { return string.Empty; }
            }

            
            return baseStyle;
        }
        public static string GetBaseStyle(this string value)
        {
            // override with a default value of 5 charectors //
            return value.GetBaseStyle(5, false);
        }

        public static bool IsAlphaNum(this string str)
        {
            if (string.IsNullOrEmpty(str))
                return false;

            return (str.ToCharArray().All(c => Char.IsLetter(c) || Char.IsNumber(c)));
        }
        public static bool IsNumber(this string str)
        {
            if (string.IsNullOrEmpty(str))
                return false;

            return (str.ToCharArray().All(c => Char.IsNumber(c)));
        }

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

        public static DateTime CTracToDateTime(this string str)
        {
            return DateTime.ParseExact(str, "yyyyMMdd",
                System.Globalization.CultureInfo.InvariantCulture,
                System.Globalization.DateTimeStyles.None);
        }  
    }
}
