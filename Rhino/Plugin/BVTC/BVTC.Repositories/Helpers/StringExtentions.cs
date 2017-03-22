using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

using System.CodeDom.Compiler;
using System.CodeDom;
using System.IO;




namespace BVTC.Repositories
{
    public static class StringExtentions
    {
        private static readonly Regex regexForTableName = new Regex(@"^[\p{L}_][\p{L}\p{N}@$#_]{0,127}$");

        public static bool ValidateTableName(this string tableName)
        {
            return regexForTableName.IsMatch(tableName);
        }

        public static string cleanString(string input)
        {
            string literal = "";
            using (var writer = new StringWriter())
            {
                using (var provider = CodeDomProvider.CreateProvider("CSharp"))
                {
                    provider.GenerateCodeFromExpression(new CodePrimitiveExpression(input), writer, null);
                    literal = writer.ToString();
                }
            }
            Regex re = new Regex("[;\\\\/:*?\"<>|']");
            string outputString = re.Replace(literal, "");
            return outputString;
        }
        public static string correctStringOneAnd(string input)
        {
            string result = input;
            if (input.Contains("&&"))
            {
                string newStr = input.Replace("&&", "&");
                result = newStr;
            }
            result = cleanString(result);
            return result;
        }
        public static string correctStringTwoAnds(string input)
        {
            string result = input;
            if (input.Contains("/"))
            {
                string newStr = input.Replace("/", "&&");
                result = newStr;
            }
            if (input.Contains(@"\"))
            {
                string newStr = input.Replace(@"\", "&&");
                result = newStr;
            }
            result = cleanString(result);
            return result;
        }
    }
}
