using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Reflection;

namespace BVTC.Data.Helpers
{
    public static class ListExtensions
    {
        public static string Compare_BaseStyle(this List<data> dataList)
        {
            if (dataList.Count < 1)
            {
                throw new Exceptions.DataMissing_Exception("No data exists in data list.");
            }

            List<string> baseStyles = new List<string>();
            List<string> blockIDs = new List<string>();
            // iterate through all units from drawing data //
            foreach (data d in dataList)
            {
                if (d.IsDeleted() == false)
                {
                    blockIDs.Add(d.GetBlockID());
                    baseStyles.Add(d.GetBaseStyle());
                }
            }

            // make sure all block ids are unique //
            if (blockIDs.Distinct().Count() != blockIDs.Count)
            {
                throw new Exceptions.BlockID_Exception("All Block IDs must be unique.");
            }

            // make sure first block is a valid entry //
            if (baseStyles[0] == "" || baseStyles[0] == null)
            {
                throw new Exceptions.BlockID_Exception("The first Block ID cannot be blank.");
            }
            // make sure all base styles match //
            else if(baseStyles.Distinct().Count() == 1)
            {
                return baseStyles[0];
            }
            else
            {
                throw new Exceptions.DataMisMatch_Exception(string.Format(
                    "All block styles: [{0}] do not share a base style", string.Join(",", baseStyles)));
            }
        }

        public static List<data> AbstractList(this List<Drafting> parent)
        {
            List<data> list = new List<data>();

            foreach (Drafting drafting in parent)
            {
                data abs = (data)drafting;
                list.Add(abs);
            }

            return list;
        }

        // helper method for comboBox Lists //
        public static string Find_String(this List<string> list, string value)
        {
            if (list.Contains(value))
            {
                int index = list.IndexOf(value);
                return list[index];
            }
            else
            {
                if (list[0] == "None" || list[0] == "") { return null; }
                else { return list[0]; }
            }
        }

        public static int TryIndexOf(this List<string> list, string find)
        {
            int index = list.IndexOf(find);
            if (list.Count < 1) { throw new Exception("List does not contain values."); }
            if (index < 0) { return 0; }
            else { return index; }
        }

        public static bool AllValuesMatch(this List<data> list, string propName, Type type, bool throwError)
        {
            int first = list.FindValidProperty(propName);

            // if no data in properties return false //
            if (first == -1)
            {
                // if all values are null throw an error //
                if (throwError)
                {
                    throw new Exceptions.DataMissing_Exception(string.Format("All values in the {0} property are null or empty.", propName));
                }
                // if all values are null, return true //
                else { return true; }


            }

            for (int i = 0; i < list.Count; i++)
            {
                var value = list[i].GetType().GetProperty(propName).GetValue(list[i]);
                string strValue = "";
                if (value != null) { strValue = value.ToString(); }
                string control = list[first].GetType().GetProperty(propName).GetValue(list[first]).ToString();
                

                if (strValue != control)
                {
                    return false;
                }
            }

            return true;
        }

        public static int FindValidProperty(this List<data> list, string propName)
        {
            int first = -1;

            // find first value with 
            for (int i = 0; i < list.Count; i++)
            {
                if (first == -1 && list[i].HasProperty(propName) == true)
                {
                    if (list[i].HasData(propName) == true)
                    {
                        first = i;
                        break;
                    }
                    else
                    {
                        list[i].GetType().GetProperty(propName).SetValue(list[i], null);
                    }
                }
                else
                {
                    throw new Exceptions.DataMisMatch_Exception(string.Format("{0} is missing from a memeber of the data list."));
                }
            }
            return first;
        }

        public static string LevenshteinFind(this List<string> list, string find)
        {
            string closest = "";

            // start a high match number //
            int match = find.Length * 10;

            foreach (string item in list)
            {
                int calc = LevenshteinDistance.Compute(item, find);
                if (calc == 0) { return item; }
                if (calc < match)
                {
                    closest = item;
                    match = calc;
                }
            }

            return closest;
        }
    }
}
