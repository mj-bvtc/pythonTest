using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Data;

using BVTC.Data.Helpers;

namespace BVTC.Data
{
    public class DataTools
    {
        public static DataTable CompareClasses(List<BVTC.Data.data> dataList, List<string> include, List<string> exclude)
        {
            DataTable dt = new DataTable();
            List<string> colList = new List<string>();

            // if there is no data to compare, return empty data table //
            if (dataList.Count <= 1) { return dt; }

            // get a list of non-null properties //
            Dictionary<string, Type> fields = new Dictionary<string, Type>();

            for (int i = 0; i < dataList.Count; i++)
            {
                foreach (PropertyInfo property in dataList[i].GetType().GetProperties())
                {
                    if ((dataList[i].HasData(property.Name) == true 
                        && fields.ContainsKey(property.Name) == false 
                        && exclude.Contains(property.Name) == false) 
                        || include.Contains(property.Name) == true
                        && fields.ContainsKey(property.Name) == false)
                    {
                        fields.Add(property.Name, property.PropertyType);
                    }
                }
            }

            foreach (KeyValuePair<string, Type> field in fields)
            {
                int validProp = dataList.FindValidProperty(field.Key);
                bool match = dataList.AllValuesMatch(field.Key, field.Value, false);

                if (match == false || (match == true && validProp >= 0 && include.Contains(field.Key) == true))
                {
                    dt.Columns.Add(new DataColumn(field.Key, field.Value));
                }
                
            }

            // add data to the DataTable //
            for (int i = 0; i < dataList.Count; i++)
            {
                DataRow row = dt.NewRow();
                for (int j = 0; j < dt.Columns.Count; j++)
                {
                    PropertyInfo property = dataList[i].GetType().GetProperty(dt.Columns[j].ColumnName);
                    if (property != null)
                    {
                        row[dt.Columns[j]] = property.GetValue(dataList[i], null);
                    }
                }
                dt.Rows.Add(row);
                row.AcceptChanges();
            }

            return dt;
        }
        public static DataTable CompareClasses(List<BVTC.Data.data> dataList)
        {
            List<Data.data> listCopy = dataList;
            

            // list of properties of include regardless of match status //
            List<string> include = new List<string>();
            include.Add("BlockID");
            //include.Add("Glaze"); **removed 2-22-17**
            include.Add("Quantity");
            include.Add("ClientID");

            // list of properties to exclude  regardless of match status //
            List<string> exclude = new List<string>();
            exclude.Add("Weight");
            exclude.Add("Volume");
            exclude.Add("EstimatingID");
            exclude.Add("SurveyID");
            exclude.Add("InitBlockID");
            exclude.Add("deleted");
            exclude.Add("DescRegion");

            // exclude styles that have been deleted from the table //
            List<Data.data> remove = new List<data>();
            foreach (Data.data data in dataList)
            {
                if (data.HasProperty("deleted") == true)
                {
                    if ((bool)data.GetType().GetProperty("deleted").GetValue(data) == true)
                    {
                        remove.Add(data);
                    }
                }
            }

            foreach (Data.data item in remove)
            {
                listCopy.Remove(item);
            }

            return CompareClasses(listCopy, include, exclude);
        }

    }
}
