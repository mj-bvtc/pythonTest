using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing.Printing;

namespace BVTC.osTools
{
    public static class PrinterTools
    {
        public static List<string> GetPrinters()
        {
            List<string> printers = new List<string>();
            foreach (string printer in System.Drawing.Printing.PrinterSettings.InstalledPrinters)
            {
                printers.Add(printer);
            }
            return printers;
        }

        public static List<string> PdfPrinters()
        {
            // create list of printers in order we want to try using them //
            return new List<string>
            {
                "FreePDF - ToDesktop",
                "Bluebeam PDF",
                "Adobe PDF"
            };
        }
        
        public static bool HasPaperSize(string printerName, double width, double height, bool throwException = true, string units = "inches")
        {
            // check to make sure the desired printer exists //
            if (GetPrinters().Contains(printerName) == false)
            {
                if (throwException)
                {
                    // throw an exception if the requested printer can't be found //
                    throw new Exceptions.PrinterMissing(string.Format(
                        "Printer named {0} is not installed on the current PC.", printerName));
                }
                // just return false //
                else { return false; }
            }


            PrinterSettings settings;
            settings = new PrinterSettings();
            settings.PrinterName = printerName;

            // scale width and height for units //
            if (units == "inches")
            {
                width = (int) Math.Round(width * 100);
                height = (int) Math.Round(height * 100);
            }

            foreach (PaperSize paperSize in settings.PaperSizes)
            {
                if (paperSize.Width == width && paperSize.Height == height)
                {
                    return true;
                }

            }
            return false;
        }

    }
}
