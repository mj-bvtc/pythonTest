using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;

namespace BVTC.Repositories.Helpers
{
    public static class DataTableExtensions
    {
        public static void TrimHeadings(this System.Data.DataTable dt)
        {
            // trim quotes from column headings //
            foreach (DataColumn col in dt.Columns)
            {
                col.ColumnName = col.ColumnName.Trim('"');
            }
        }

        public static void TrimWhiteSpace(this System.Data.DataTable dt)
        {
            for (int i = 0; i < dt.Columns.Count; i++)
            {
                if (dt.Columns[i].DataType == typeof(string))
                {
                    foreach (DataRow row in dt.Rows)
                    {
                        string value = (string)row[i];
                        row[i] = value.Trim();
                    }
                }
            }
            dt.AcceptChanges();
        }

        public static List<string> GetHeadings(this System.Data.DataTable dt, bool removeQuotes=false)
        {
            List<string> headings = new List<string>();
            foreach (DataColumn col in dt.Columns)
            {
                string colName = col.ColumnName;
                if (removeQuotes == true) { colName = col.ColumnName.Replace('"'.ToString(), string.Empty); }
                headings.Add(colName);
            }
            return headings;
        }

        public static void StripHeadings(this System.Data.DataTable dt, string strip)
        {
            for (int i = 0; i < dt.Columns.Count; i++)
            {
                if (dt.Columns[i].ColumnName.Substring(0,strip.Length) == strip)
                {
                    dt.Columns[i].ColumnName = dt.Columns[i].ColumnName.Substring(
                        strip.Length, dt.Columns[i].ColumnName.Length - strip.Length);
                }
            }
            dt.AcceptChanges();
        }

        public static void AlphabetizeColumns(this System.Data.DataTable dt)
        {
            List<string> headings = dt.GetHeadings();
            headings.Sort();

            for (int i = 0; i < dt.Columns.Count; i++)
            {
                dt.Columns[i].SetOrdinal(headings.IndexOf(dt.Columns[i].ColumnName));
            }
            dt.AcceptChanges();
        }
    }
}
