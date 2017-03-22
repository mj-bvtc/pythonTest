using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.UI
{
    public class ComboLists
    {
        // forming method //
        private List<string> formingMethod { get; set; }
        public List<string> DescFormingMethod
        {
            get
            {
                // check if data exists //
                if (this.formingMethod != null)
                {
                    if (this.formingMethod.Count > 0)
                    {
                        return this.formingMethod;
                    }
                }

                // get data, save and return it //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.formingMethod = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1}", "FormingMethod", "DescFormingMethod"));
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }

                return this.formingMethod;
            }
        }

        // Orientation //
        private List<string> orientation { get; set; }
        public List<string> DescOrientation
        {
            get
            {
                // check if data is already stored //
                if (this.orientation != null)
                {
                    if (this.orientation.Count > 0)
                    {
                        return this.orientation;
                    }
                }

                // get, store and return data //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.orientation = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1} ORDER BY {0}", "Orientation", "DescOrientation"));
                    this.orientation.Insert(0, "");
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.orientation;
            }
        }

        // sculpture //
        private List<string> scultpure { get; set; }
        public List<string> DescSculpture
        {
            get
            {
                // check if data is present //
                if (this.scultpure != null)
                {
                    if (this.scultpure.Count > 0)
                    {
                        return this.scultpure;
                    }
                }

                // get, save and return data //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.scultpure = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1} ORDER BY {2}", "Sculpture", "DescSculpture", "Value"));
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.scultpure;
            }
        }

        // Shape //
        private List<string> shape { get; set; }
        public List<string> DescShape
        {
            get
            {
                // check if data is stored //
                if (this.shape != null)
                {
                    if (this.shape.Count > 0)
                    {
                        return this.shape;
                    }
                }

                // find, save and return data //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.shape = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1} ORDER BY {0}", "Shape", "DescShape"));
                    this.shape.Insert(0, "");
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.shape;
            }
        }

        // Style //
        private List<string> style { get; set; }
        public List<string> DescStyle
        {
            get
            {
                // check if data is stored //
                if (this.style != null)
                {
                    if (this.style.Count > 0)
                    {
                        return this.style;
                    }
                }
                
                // find, store and return data //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.style = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1} ORDER BY {0}", "Style", "DescStyle"));
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.style;
            }
        }

        // User Names //
        private List<string> names { get; set; }
        public List<string> DrafterNames
        {
            get
            {
                if (this.names != null)
                {
                    if (this.names.Count > 0)
                    {
                        return this.names;
                    }
                }

                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.names = CTrac.CommandToList("CALL Get_DrafterNames()");
                    this.names.Insert(0, "None");
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.names;
            }
        }

        // User Initials //
        private List<string> initials { get; set; }
        public List<string> DrafterInitials
        {
            get
            {
                // check if data is present //
                if (this.initials != null)
                {
                    if (this.initials.Count > 0)
                    {
                        return this.initials;
                    }
                }

                // get data, save return it //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.initials = CTrac.CommandToList("CALL Get_DrafterInitials()");
                    this.initials.Insert(0, "");
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.initials;
            }
        }

        // Regions //
        private List<string> regions { get; set; }
        public List<string> DescRegion
        {
            get
            {
                // check if data is present //
                if (this.regions != null)
                {
                    if (this.regions.Count > 0)
                    {
                        return this.regions;
                    }
                }

                // get data, save return it //
                Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
                try
                {
                    this.regions = CTrac.CommandToList(string.Format(
                        "SELECT {0} FROM {1} ORDER BY {0}", "Region", "DescRegion"));
                }
                catch (Exception e)
                {
                    throw e;
                }
                finally
                {
                    CTrac.CloseDB();
                }
                return this.regions;
            }
        }
    }
}
