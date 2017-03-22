using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;

namespace BVTC.Data.Helpers
{
    public static class DataExtensions
    {
        public static string GetBlockID(this data d)
        {
            /* Check data class has "BlockID" property.
             * Check data.BlockID is a string type.
             * Return:
             *      string - data.BlockID();
             * Exceptions:
             *      DataMisMatch_Exception - data.BlockID isn't a string.
             *      DataMissing_Exception - data does not contain "BlockID" property.
             *      BlockID_Exception - the string is not a properly formatted Block ID.
             */

            string propName = "BlockID";
            if (d.HasProperty(propName) == true)
            {
                PropertyInfo prop = d.GetType().GetProperty(propName);
                if (prop.PropertyType.GetType() != typeof(string))
                {
                    return (string)prop.GetValue(d, null);
                }
                else
                {
                    throw new Exceptions.DataMisMatch_Exception(
                        string.Format("data.{0} is not a string type. ({1})", propName, prop.PropertyType));
                }

            }
            else
            {
                throw new Exceptions.DataMissing_Exception(
                    string.Format("data class is missing a {0} property", propName));
            }
        }

        public static bool CheckBlockID(this data d)
        {
            /* Check data class has "BlockID" property.
             * Check data.BlockID is a string type.
             * Return:
             *      bool - string.CheckBlockID();
             * Exceptions:
             *      DataMisMatch_Exception - data.BlockID isn't a string.
             *      DataMissing_Exception - data does not contain "BlockID" property.
             *      BlockID_Exception - the string is not a properly formatted Block ID.
             */

            string propName = "BlockID";
            bool verified = true;
            if (d.HasProperty(propName) == true)
            {
                PropertyInfo prop = d.GetType().GetProperty(propName);
                if (prop.PropertyType != typeof(string))
                {
                    string value = (string)prop.GetValue(d, null);
                    verified = value.CheckBlockID();
                }
                else
                {
                    throw new Exceptions.DataMisMatch_Exception(
                        string.Format("data.{0} is not a string type. ({1})", propName, prop.PropertyType));
                }

            }
            else
            {
                throw new Exceptions.DataMissing_Exception(
                    string.Format("data class is missing a {0} property", propName));
            }
            return verified;
        }

        public static string GetBaseStyle(this data d)
        {
            /* Check data class has "BlockID" property.
             * Check data.BlockID is a string type.
             * Return:
             *      bool - string.CheckBlockID();
             * Exceptions:
             *      DataMisMatch_Exception - data.BlockID isn't a string.
             *      DataMissing_Exception - data does not contain "BlockID" property.
             *      BlockID_Exception - the string is not a properly formatted Block ID.
             */

            return GetBlockID(d).GetBaseStyle();

            /* #####################
             * ## removed 12-6-16 ##
             * #####################
             * 
             * No longer needed, migrated to data.GetBlockID()
             *
            string propName = "BlockID";
            if (d.HasProperty(propName) == true)
            {
                PropertyInfo prop = d.GetType().GetProperty(propName);
                if (prop.PropertyType.GetType() != typeof(string))
                {
                    string value = (string)prop.GetValue(d, null);
                    return value.GetBaseStyle();
                }
                else
                {
                    throw new Exceptions.DataMisMatch_Exception(
                        string.Format("data.{0} is not a string type. ({1})", propName, prop.PropertyType));
                }

            }
            else
            {
                throw new Exceptions.DataMissing_Exception(
                    string.Format("data class is missing a {0} property", propName));
            }
            */
        }

        public static bool IsDeleted(this data d)
        {
            /* Check data class has "deleted" property.
             * Check data.BlockID is a string type.
             * Return:
             *      string - data.BlockID();
             * Exceptions:
             *      DataMisMatch_Exception - data.BlockID isn't a string.
             *      DataMissing_Exception - data does not contain "BlockID" property.
             *      BlockID_Exception - the string is not a properly formatted Block ID.
             */

            string propName = "deleted";
            if (d.HasProperty(propName) == true)
            {
                PropertyInfo prop = d.GetType().GetProperty(propName);
                if (prop.PropertyType.GetType() != typeof(bool))
                {
                    return (bool)prop.GetValue(d, null);
                }
                else
                {
                    throw new Exceptions.DataMisMatch_Exception(
                        string.Format("data.{0} is not a bool type. ({1})", propName, prop.PropertyType));
                }

            }
            else
            {
                throw new Exceptions.DataMissing_Exception(
                    string.Format("data class is missing a {0} property", propName));
            }
        }
    }
}
