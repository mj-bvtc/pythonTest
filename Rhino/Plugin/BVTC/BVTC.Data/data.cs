using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data;
using System.Reflection;
using Pervasive.Data.SqlClient;

using BVTC.Data.Helpers;

namespace BVTC.Data
{
    public abstract class data
    {
        public data()
        {/* create blank data class */}
        public data(data d)
        {
            /* create data class from another class. 
             * will copy over matching properties from derived classes.
             */
            Update(d);
        }
        public data(DataRow row)
        {
            Update(row);
        }

        public bool HasProperty(string propName)
        {
            return this.GetType().GetProperty(propName) != null;
        }
        public bool HasData(string propName)
        {
            if (this.HasProperty(propName) == false)
            {
                return false;
            }

            var value = this.GetType().GetProperty(propName).GetValue(this, null);

            // if object is null //
            if (value == null)
            {
                return false;
            }

            // if value is a string //
            if (value.GetType() == typeof(string))
                if ((string)value == "" || (string)value == null)
                    return false;


            // sufficient data exists in property //
            return true;
        }

        public void Update(DataRow row)
        {
            /* Update Revision Data from DataRow
             * match row columns names to class properties.
             */

            // loop through columns in row //
            for (int i = 0; i < row.Table.Columns.Count; i++)
            {
                string colName = row.Table.Columns[i].ColumnName;
                colName = colName.classFormat();
                var value = row[i];

                if (this.HasProperty(colName) == true)
                {
                    // get mapped property from class //
                    PropertyInfo property = this.GetType().GetProperty(colName);

                    // trim white space from behind CHAR() data //
                    if (property.PropertyType == typeof(string) && value.GetType() == typeof(string))
                    {
                        value = ((string)value).Trim();
                    }
                        
                    

                    // convert number zero into false //
                    if (property.PropertyType == typeof(bool) && value.GetType() == typeof(System.Int16))
                    {
                        System.Int16 test = (Int16)value;
                        if (test == 0) { value = false; }
                        else { value = true; }
                    }

                    // convert CHAR(8) into System.DateTime //
                    if (property.PropertyType == typeof(DateTime) && value.GetType() == typeof(string))
                    {
                        string date = (string)value;
                        value = date.CTracToDateTime();
                    }

                    try
                    {
                        property.SetValue(this, value, null);
                    }
                    catch
                    {
                        // column mis-match error //
                        throw new Exceptions.DataMisMatch_Exception(
                            string.Format("Column type mismatch: {0}, {1}", colName, value.ToString()));
                    }
                }
                else
                {
                    // unable to set text property //
                    throw new Exceptions.DataMisMatch_Exception(
                            string.Format("Could not place data: '{0}' in class: '{1}'", value, colName));
                }
            }
        }
        public void Update(data d)
        {
            /* Find similar properties between classes
             * Migrate data from input to this data class.
             */
            foreach (PropertyInfo property in d.GetType().GetProperties())
            {
                // check to make sure both classes the same property //
                if (this.HasProperty(property.Name) == true)
                {
                    // make sure the data types match //
                    if (this.GetType().GetProperty(property.Name).GetType() == property.GetType())
                    {
                        // set property from input data class into this data class //
                        this.GetType().GetProperty(property.Name).SetValue(this, property.GetValue(d, null), null);
                    }
                }
            }
        }

        public void Combine(data d, List<string> sum, List<string> key, List<string> max, List<string> none)
        {
            foreach (PropertyInfo property in d.GetType().GetProperties())
            {

                if (this.HasProperty(property.Name))
                {
                    if (property.PropertyType == this.GetType().GetProperty(property.Name).PropertyType)
                    {
                        // sum the property into this class (will only work with number properties) //
                        if (sum.Contains(property.Name))
                        {
                            // add float values //
                            if (property.PropertyType == typeof(float))
                            {
                                float first = (float)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                float second = (float)property.GetValue(d, null);
                                this.GetType().GetProperty(property.Name).SetValue(this, first + second, null);
                            }

                            // add int values //
                            else if (property.PropertyType == typeof(int) || property.PropertyType == typeof(System.Int32))
                            {
                                int first = (int)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                int second = (int)property.GetValue(d, null);
                                this.GetType().GetProperty(property.Name).SetValue(this, first + second, null);
                            }

                            // add double values //
                            else if (property.PropertyType == typeof(double))
                            {
                                double first = (double)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                double second = (double)property.GetValue(d, null);
                                this.GetType().GetProperty(property.Name).SetValue(this, first + second, null);
                            }
                            else
                            {
                                try
                                {
                                    int first = (int)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                    int second = (int)property.GetValue(d, null);
                                    this.GetType().GetProperty(property.Name).SetValue(this, first + second, null);
                                }
                                catch
                                {
                                    // not a number error //
                                    throw new Exceptions.DataMisMatch_Exception(
                                        string.Format("Not a number."));
                                }
                            }
                        }

                        // put the max value into this class (will only work with number properties) //
                        if (max.Contains(property.Name))
                        {
                            // if property is an int //
                            if (property.PropertyType == typeof(int))
                            {
                                int first = (int)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                int second = (int)property.GetValue(d, null);
                                if (first < second)
                                    this.GetType().GetProperty(property.Name).SetValue(this, second, null);
                                else
                                    this.GetType().GetProperty(property.Name).SetValue(this, first, null);
                            }
                            // if property is a double //
                            if (property.PropertyType == typeof(double))
                            {
                                double first = (double)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                double second = (double)property.GetValue(d, null);
                                if (first < second)
                                    this.GetType().GetProperty(property.Name).SetValue(this, second, null);
                                else
                                    this.GetType().GetProperty(property.Name).SetValue(this, first, null);
                            }
                            // if property is an float //
                            if (property.PropertyType == typeof(float))
                            {
                                float first = (float)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                float second = (float)property.GetValue(d, null);
                                if (first < second)
                                    this.GetType().GetProperty(property.Name).SetValue(this, second, null);
                                else
                                    this.GetType().GetProperty(property.Name).SetValue(this, first, null);
                            }
                        }

                        // make mis-match data blank (only works on string properties) //
                        if (none.Contains(property.Name))
                        {
                            // see if values match //
                            var first = this.GetType().GetProperty(property.Name).GetValue(this, null);
                            var second = property.GetValue(d, null);
                            // if value don't match set empty string //
                            if (first != second)
                                this.GetType().GetProperty(property.Name).SetValue(this, "", null);
                        }

                        // mis-matched data should refer user to a key //
                        if (key.Contains(property.Name))
                        {
                            if (property.PropertyType == typeof(string))
                            {
                                // if value don't match set value = "SEE KEY" //
                                string first = (string)this.GetType().GetProperty(property.Name).GetValue(this, null);
                                string second = (string)property.GetValue(d, null);

                                if (string.IsNullOrEmpty(first) != string.IsNullOrEmpty(second))
                                {
                                    this.GetType().GetProperty(property.Name).SetValue(this, "SEE KEY", null);
                                }
                                else if (first != second)
                                {
                                    this.GetType().GetProperty(property.Name).SetValue(this, "SEE KEY", null);
                                }
                            }                                
                        }
                    }
                    else
                    {
                        // if there was a type mis-match //
                        throw new Exceptions.DataMisMatch_Exception(
                            string.Format("Type mis-match on property: {0}, type:{1} != {2}", property.Name));
                    }
                }
                else
                    throw new Exceptions.DataMisMatch_Exception(
                        string.Format("Property: '{0}' does not exist in this class.", property.Name));
            }
        }

        public void CorrectStrings(string[] removeList)
        {
            /* correct all string values to remove bad charectors */
            PropertyInfo[] propList = this.GetType().GetProperties();

            foreach (PropertyInfo property in propList)
            {
                // trim bad charectors from behind string data //
                if (property.PropertyType == typeof(string))
                {
                    string value = (string)property.GetValue(this, null);
                    // remove bad charectors from string //
                    foreach (string remove in removeList)
                    {
                        if (value.Contains(remove) == true)
                        {
                            value = value.Replace(remove.ToString(), string.Empty);
                            // set new value into property //
                            property.SetValue(this, value, null);
                        }
                    }
                }
            }
        }
        public void CorrectStrings()
        {
            // overloaded class for ease of use //
            // correct with default list of values //
            string[] badChars = new string[] { "'", ",", "@", ";", '"'.ToString() };
            CorrectStrings(badChars);
        }

        public data Duplicate()
        {
            /* Create a duplicate of the data class
             * Used to create added tabs
             */
            return (data)this.MemberwiseClone();
        }

        public string OutputString(string propName)
        {
            PropertyInfo prop = this.GetType().GetProperty(propName);
            if (prop != null)
            {
                // format DateTime to MM-DD-YYYY //
                if (prop.PropertyType == typeof(DateTime))
                {
                    DateTime value = (DateTime)prop.GetValue(this, null);
                    return value.ToShortDateString();
                }

                return prop.GetValue(this, null).ToString();

            }
            return "";
        }

        /*
         * // Removed 10-28-16 in attempt to compile //
        public PsqlCommand InsertCommand(dbTools.CTrac_dbTools CTrac, string table)
        {

            // get table columns from C-Trac //
            List<string> headings = CTrac.Get_ColumnNames(table, true);

            // new lists //
            List<string> columns = new List<string>();
            List<string> paramStrings = new List<string>();

            // list of values to insert //
            List<PsqlParameter> parameters = new List<PsqlParameter>();
            // list of table values //
            List<PsqlDbType> dbTypes = CTrac.Table_DateTypes(table);

            //for (int i = 0; i < headings.Count; i++)
            for (int i = 0; i < headings.Count; i++)
            {
                // make sure the class property exists //
                string className = headings[i].Replace(" ", string.Empty).Trim('"');
                if (this.HasProperty(className))
                {
                    // make sure the value of the property is not null //
                    var value = this.GetType().GetProperty(className).GetValue(this, null);
                    if (value != null)
                    {
                        columns.Add(headings[i]);
                        paramStrings.Add("?");

                        // create new parameter //
                        PsqlParameter param = new PsqlParameter();
                        param.PsqlDbType = dbTypes[i];

                        // DateTime => CHAR(8) //
                        if (value.GetType() == typeof(DateTime) && dbTypes[i] == PsqlDbType.Char)
                        {
                            DateTime dt = (DateTime)value;
                            value = dt.CTracFormat();
                        }

                        // bool => 0 or 1 //
                        if (value.GetType() == typeof(bool) && dbTypes[i] == PsqlDbType.Bit)
                        {
                            if ((bool)value == true) { value = 1; }
                            else { value = 0; }
                        }

                        param.Value = value;
                        parameters.Add(param);
                    }
                }
            }

            // format command string with '?'s //
            string cmdStr = "INSERT INTO " + table + " (";
            cmdStr += string.Join(", ", columns);
            cmdStr += ") VALUES (" + string.Join(", ", paramStrings) + ")";

            // create command and add parameters //
            PsqlCommand cmd = new PsqlCommand(cmdStr, CTrac.conn);
            foreach (PsqlParameter param in parameters)
            {
                cmd.Parameters.Add(param);
            }

            return cmd;
        }
        */
    }
}
