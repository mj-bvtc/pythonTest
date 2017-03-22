using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Data;

using System.Reflection;
using System.ComponentModel;

using BVTC;
using BVTC.Data.Helpers;
using BVTC.Repositories.Helpers;
using Pervasive.Data.SqlClient;


namespace BVTC.Data
{
    public class Drafting : data
    {
        // constructor methods //
        public Drafting()
        {
            this.deleted = false;
        }
        public Drafting(data d) : base(d)
        { /* inherit constructor from abstract base class,
           * I am pretty proud of myself for this one. 
           * -PAS-
           */
        }
        public Drafting(DataRow d) : base(d) { }

        public bool Updated { get; set; }
        public string ProjectNumber { get; set; }
        public string Pcode { get; set; }
        public string ShortDescription { get; set; }

        // custom get & set methods //
        private string blockID { get; set; }
        public string BlockID
        {
            get { return this.blockID; }
            set
            {
                this.blockID = value;
                this.BaseStyle = value.GetBaseStyle();
            }
        }

        public string InitBlockID { get; set; }

        // custom get & set methods //
        private string baseStyle { get; set; }
        public string BaseStyle
        {
            get { return this.baseStyle; }
            set
            {
                this.baseStyle = value;
            }
        }
        
        public string Sample { get; set; }

        public string User { get; set; }
        public string CheckedBy { get; set; }
        public DateTime DateCreated { get; set; }
        public string Status { get; set; }

        public string EstimatingID { get; set; }
        public string ClientID { get; set; }
        public string SurveyID { get; set; }

        // removed 11-29-16 //
        // public string DrawingNumber { get; set; } 

        public int DrawingSub { get; set; }
        public string Revision { get; set; }

        public int Quantity { get; set; }
        public string Glaze { get; set; }

        public string DescStyle { get; set; }
        public string DescShape { get; set; }
        public string DescSculpture { get; set; }
        public string DescOrientation { get; set; }
        public string DescRegion { get; set; }

        public string Profile { get; set; }
        public string DescFormingMethod { get; set; }
        public string Comments { get; set; }

        private double length { get; set; }
        public double Length
        {
            get { return this.length; }
            set { this.length = Math.Round(value, 3); }
        }

        private double height { get; set; }
        public double Height
        {
            get { return this.height; }
            set { this.height = Math.Round(value, 3); }
        }

        private double depth { get; set; }
        public double Depth
        {
            get { return this.depth; }
            set { this.depth = Math.Round(value, 3); }
        }

        private double volume { get; set; }
        public double Volume
        {
            get { return this.volume; }
            set { this.volume = Math.Round(value, 3); }
        }

        public double Weight
        {
            get { return Math.Round(this.volume * 0.082, 3); }
            set { }
        }

        public double Scale { get; set; }

        public string Path { get; set; }
        public string GUID { get; set; }

        public bool deleted { get; set; }

        public void SetAttr_FromTextBox(string propName, string text)
        {
            if (this.HasProperty(propName) == false)
            {
                throw new ArgumentNullException(string.Format("property name: '{0}' does not exist in current class."));
            }

            // get the property type //
            Type propType = this.GetType().GetProperty(propName).PropertyType;
            // create a type converter for that type //
            TypeConverter typeconverter = TypeDescriptor.GetConverter(propType);

            try
            {
                // convert string to object //
                object propValue = typeconverter.ConvertFromString(text);
                // set property in this class to converted object //
                this.GetType().GetProperty(propName).SetValue(this, propValue);
            }
            catch (Exception)
            {
                throw new Exceptions.DataMisMatch_Exception(string.Format(
                    "Could not format value: {0} into type: {1}", text, propType));
            }

            // set update to true //
            this.Updated = true;
            
        }

        public void Combine(data d)
        {
            // make rule lists for combining classes //
            List<string> sum = new List<string>();
            sum.Add("Quantity");

            List<string> key = new List<string>();
            key.Add("Glaze");
            key.Add("Sample");

            List<string> max = new List<string>();
            max.Add("Weight");

            List<string> none = new List<string>();
            none.Add("DescSculpture");
            none.Add("DescOrientation");
            none.Add("DescShape");
            none.Add("DescStyle");
            

            Combine(d, sum, key, max, none);
        }
        // insert some test data //
        public void testData()
        {
            /* Set up dome data to Test with offline. */
            this.Updated = true;
            this.ProjectNumber = "P12-3445";
            this.ShortDescription = "Test Project";

            this.BlockID = "A1-1";
            this.BaseStyle = "A1";
            this.Sample = "A1";
            this.EstimatingID = "EST-12-ICOC";
            this.ClientID = "CLT-12-C";

            this.User = "PAS";
            this.DateCreated = DateTime.Today;
            this.Status = "DRAWN";

            this.Quantity = 10;
            this.Glaze = "Red";
            this.DescStyle = "Ashlar";
            this.DescShape = "Corner";
            this.DescSculpture = "High Running";
            this.DescOrientation = "Middle";
            this.Profile = "None";
            this.DescFormingMethod = "HP";

            this.Comments = "No Comment";

            this.Length = 9;
            this.Height = 10;
            this.Depth = 11;
            this.Volume = 100;
            this.Scale = .5;

            this.Path = @"C:\Users\BVTC Remote\Desktop\Test.file";
            this.GUID = "0000-TEST-GUID-HERE-0000";

            // Test what happens to null values //
            //this.DrawingNumber = 1;
            //this.DrawingSub = 1;
        }

        public string UpsertCTrac()
        {
            // create a list of properties to add to upsert command //
            List<string> values = new List<string>();

            List<string> propNames = new List<string>();
            propNames.Add("Updated");
            propNames.Add("deleted");
            propNames.Add("ProjectNumber");
            propNames.Add("BlockID");
            propNames.Add("InitBlockID");
            propNames.Add("BaseStyle");
            propNames.Add("Sample");
            propNames.Add("User");
            propNames.Add("CheckedBy");
            propNames.Add("DateCreated");
            propNames.Add("Status");
            propNames.Add("EstimatingID");
            propNames.Add("ClientID");
            propNames.Add("SurveyID");
            //propNames.Add("DrawingNumber"); **removed 11-29-16**
            propNames.Add("DrawingSub");
            propNames.Add("Quantity");
            propNames.Add("Glaze");
            propNames.Add("DescStyle");
            propNames.Add("DescShape");
            propNames.Add("DescSculpture");
            propNames.Add("DescOrientation");
            propNames.Add("Profile");
            propNames.Add("DescFormingMethod");
            propNames.Add("Comments");
            propNames.Add("Length");
            propNames.Add("Height");
            propNames.Add("Depth");
            propNames.Add("Volume");
            propNames.Add("Weight");
            propNames.Add("Scale");
            propNames.Add("Path");
            propNames.Add("GUID");
            propNames.Add("DescRegion");

            // loop through this properties and skip specific items //
            foreach (string propName in propNames)
            {
                PropertyInfo prop = this.GetType().GetProperty(propName);
                if (prop != null)
                {
                    var obj = prop.GetValue(this);
                    values.Add(obj.PervasiveFormat(prop.PropertyType));
                }
                else
                {
                    throw new Exceptions.DataMissing_Exception(string.Format("class has no property: {0}", propName));
                }
            }
            string cmd = "CALL Upsert_Drafting(";
            cmd += string.Join(", ", values) + ")";

            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
            try
            {
                CTrac.ExecuteCommand(cmd);
            }
            catch (Exception e)
            {
                throw e;
            }
            finally
            {
                CTrac.CloseDB();
            }

            return cmd;
        }

        /* removed 11-29-16
        public void Set_DrawingNumber()
        {
            // if the base style is changed recalculate drawing name //
            this.DrawingNumber = this.Pcode + '-' + this.BaseStyle;
        }
        */
    }
}
