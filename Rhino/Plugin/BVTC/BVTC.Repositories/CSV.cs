using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data;
using System.IO;

namespace BVTC.Repositories
{
    class CSV
    {
        public void dataTableToCSV(string path, DataTable dt)
        {
            /* Create a CSV file from a dataTable and a file path
             * General utility creating csv files.
             */
            List<string> lines = new List<string>();

            List<string> colHeadings = new List<string>();
            foreach (DataColumn col in dt.Columns)
            {
                string name = col.ColumnName.ToString();
                colHeadings.Add(name);
            }

            lines.Add(string.Join(",", colHeadings));

            foreach (DataRow row in dt.Rows)
            {
                List<string> items = new List<string>();
                for (int i = 0; i < dt.Columns.Count; i++)
                {
                    items.Add(row[i].ToString().Trim());
                }
                lines.Add(string.Join(",", items));
            }
            try
            {
                // over write file //
                File.Delete(path);
                File.AppendAllLines(path, lines);
            }
            catch
            {
                throw new Exception(string.Format("Cannot access file: {0}", path));
            }
        }
    }
}
