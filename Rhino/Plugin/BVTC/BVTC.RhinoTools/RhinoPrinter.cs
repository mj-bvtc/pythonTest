using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino;

namespace BVTC.RhinoTools
{
    public class RhinoPrinter
    {
        public RhinoDoc Doc { get; set; }
        public Rhino.Display.RhinoPageView PageView { get; set; }
        public string Printer { get; set; }

        public Tuple<double, double> PageSize { get; set; }
        public double PageWidth
        {
            get { return this.PageSize.Item2; }
        }
        public double PageHeight
        {
            get { return this.PageSize.Item1; }
        }
        public UnitSystem Units { get; set; }
        public string ViewportArea { get; set; }

        public string OutputType { get; set; }
        public string OutputColor { get; set; }

        public Tuple<double, double, double, double> Margins { get; set; }

        public bool Preview { get; set; }

        public RhinoPrinter() { }
        public RhinoPrinter(RhinoDoc doc, Rhino.Display.RhinoPageView pageView, string printer, double printHeight = 11, double printWidth = 17)
        {
            this.Doc = doc;
            this.PageView = pageView;

            // default setting for the printer //
            this.Printer = printer;
            this.Units = doc.PageUnitSystem;

            this.PageSize = new Tuple<double, double>(printHeight, printWidth);

            this.OutputType = "Raster";
            this.OutputColor = "DisplayColor";

            if (printHeight == 8.5 && printWidth == 11)
            { this.ViewportArea = "Extents"; }
            else { this.ViewportArea = "Window"; }

            this.Margins = new Tuple<double, double, double, double>(0, 0, 0, 0);

            this.Preview = false;

        }

        public void Print()
        {
            string cmd = "-_Print ";

            // enter Setup menu //
            cmd += "Setup ";

            // enter Destination menu //
            cmd += "Destination ";

            // set printer //
            if (string.IsNullOrEmpty(this.Printer) == false)
            {
                cmd += string.Format("Printer {0} ", '"' + this.Printer + '"');
            }

            // set page size //
            if (this.PageSize != null)
            {
                double width = 0;
                double height = 0;
                if (this.Units == UnitSystem.Inches)
                {
                    width = this.PageWidth * 25.4;
                    height = this.PageHeight * 25.4;
                }
                
                if (width > 0 && height > 0)
                {
                    cmd += string.Format("PageSize {0} {1} ", width, height);
                }
            }

            // calibration scale should always be 1 //
            cmd += string.Format("CalibrateXScale {0} ", 1);
            cmd += string.Format("CalibrateYScale {0} ", 1);

            // set display type (raster or vector) //
            if (string.IsNullOrEmpty(this.OutputType) == false)
            {
                cmd += string.Format("OutputType={0} ", this.OutputType);
            }

            // set display color (print, display BW) //
            if (string.IsNullOrEmpty(this.OutputColor) == false)
            {
                cmd += string.Format("OutputColor={0} ", this.OutputColor);
            }

            // exit Destination menu //
            cmd += "_Enter ";

            // enter view menu //
            cmd += "View ";
            // set view output scale //
            cmd += string.Format("Viewport {0} ", PageView.PageName);
            // set viewport area //
            if(this.ViewportArea == "Window")
            {
                cmd += string.Format("ViewportArea=Window 0,0,0 {0},{1},0 _Enter ", this.PageView.PageWidth, this.PageView.PageHeight);
                
            }
            else if (this.ViewportArea == "Extents")
            {
                cmd += string.Format("ViewportArea=Extents ");
            }
            // exit view menu //
            cmd += "_Enter ";


            // set margins //
            if (this.Margins != null)
            {
                cmd += "Margins ";
                cmd += string.Format("LeftMargin={0} ", this.Margins.Item1);
                cmd += string.Format("RightMargin={0} ", this.Margins.Item2);
                cmd += string.Format("TopMargin={0} ", this.Margins.Item3);
                cmd += string.Format("BottomMargin={0} ", this.Margins.Item4);
                cmd += "_Enter ";
            }

            // exit Setup menu //
            cmd += "_Enter ";

            // set auto printing setting //
            if (this.Preview) { cmd += "Preview "; }
            else { cmd += "Go "; }

            RhinoApp.RunScript(cmd, false);
        }

        public void OnPrintError(object source, System.IO.ErrorEventArgs args)
        {
            RhinoApp.WriteLine("Attempting to reprint PDF after error.");
            if (args.GetException().GetType() == typeof(osTools.Exceptions.BlankPDF_Exception))
            {
                // show user a preview window to correct errors //
                this.Preview = true;
                this.Print();
            }
        }
    }
}
