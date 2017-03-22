using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using PdfSharp;
using PdfSharp.Drawing;
using PdfSharp.Pdf;

namespace BVTC.osTools
{
    public class PdfTools
    {
        public static void CombinePDFs(List<string> files, string outputPath, 
            bool forceLandscape = true, bool overwrite = true)
        {

            if (System.IO.File.Exists(outputPath))
            {
                if (overwrite && !FileTools.IsFileLocked(outputPath))
                {
                    System.IO.File.Delete(outputPath);
                }
                else {
                    throw new Exceptions.FileInUse(string.Format(
                 "Cannot Overwrite: '{0}'", outputPath));
                }
            }

            // create new  output document //
            PdfSharp.Pdf.PdfDocument outputDocument = new PdfSharp.Pdf.PdfDocument();

            // Show consecutive pages facing
            outputDocument.PageLayout = PdfPageLayout.SinglePage;

            XFont font = new XFont("Verdana", 10, XFontStyle.Bold);
            XStringFormat format = new XStringFormat();
            format.Alignment = XStringAlignment.Center;
            format.LineAlignment = XLineAlignment.Far;
            XGraphics gfx;

            // Open the external documents as XPdfForm objects. Such objects are
            // treated like images. By default the first page of the document is
            // referenced by a new XPdfForm.

            foreach (string filename in files)
            {
                if (!System.IO.File.Exists(filename))
                {
                    Console.WriteLine("File does not exist {0}", filename);
                    return;
                }

                XPdfForm form = XPdfForm.FromFile(filename);

                for (int idx = 0; idx < form.PageCount; idx++)
                {
                    // Add new page to the output document
                    PdfPage page = outputDocument.AddPage();
                    // graphics object for new page //
                    gfx = XGraphics.FromPdfPage(page);

                    // if page is portrat //
                    if (form.PointHeight > form.PointWidth && forceLandscape)
                    {
                        page.Width = form.PointHeight;
                        page.Height = form.PointWidth;

                        // rotate pdf image //
                        gfx.RotateAtTransform(90, new XPoint(0, 0));
                        gfx.TranslateTransform(0, -form.PointHeight);
                    }
                    else
                    {
                        page.Width = form.PointWidth;
                        page.Height = form.PointHeight;
                    }

                    // Set page number (which is one-based)
                    form.PageNumber = idx + 1;

                    // Draw the page identified by the page number like an image
                    gfx.DrawImage(form, new XRect(0, 0, form.PointWidth, form.PointHeight));
                }

            }

            // Save the document...
            outputDocument.Save(outputPath);
        }

        public static bool RotatePDF(string pdfPath, double rotation = 90)
        {
            bool result = false;

            // create new  output document //
            PdfDocument outputDoc = new PdfSharp.Pdf.PdfDocument();

            // generate pdf form //
            XPdfForm form = XPdfForm.FromFile(pdfPath);
            
            // get all pages //
            for (int idx = 0; idx < form.PageCount; idx++)
            {
                // Add new page to the output document
                PdfPage page = outputDoc.AddPage();
                // Get a graphics object for new page //
                XGraphics gfx = XGraphics.FromPdfPage(page);

                // check if its landscape //
                if (form.PointHeight > form.PointWidth)
                {

                    page.Width = form.PointHeight;
                    page.Height = form.PointWidth;

                    gfx.RotateAtTransform(rotation, new XPoint(0, 0));
                    // this should be done with trig funcitons //
                    gfx.TranslateTransform(0, -form.PointHeight);

                    gfx.DrawImage(form, new XRect(0, 0, form.PointWidth, form.PointHeight));
                    outputDoc.Save(pdfPath);
                    return true;
                }
                else
                {
                    
                    Console.WriteLine("Landscape {0}x{1}: {2}",
                        form.PointWidth, form.PointHeight, pdfPath);
                     
                }
                
            }
            return result;
        }
    }


    public class PageSettings
    {
        public double PageWidth { get; set; }
        public double PageHeight { get; set; }
        public Collections.SubmittalTarget SubmitTo { get; set; }
        public Collections.PdfColumn PdfColumn { get; set; }
        public string PdfColumnName
        {
            get { return this.PdfColumn.ToString(); }
        }

        // initialize from submittal target //
        public PageSettings(Collections.SubmittalTarget submitTo)
        {
            if (submitTo == Collections.SubmittalTarget.Client)
            {
                this.PageHeight = 11;
                this.PageWidth = 17;
                this.PdfColumn = Collections.PdfColumn.ClientPDF;
            }
            else
            {
                this.PageHeight = 8.5;
                this.PageWidth = 11;
                this.PdfColumn = Collections.PdfColumn.ShopPDF;
            }
        }

    }
}
