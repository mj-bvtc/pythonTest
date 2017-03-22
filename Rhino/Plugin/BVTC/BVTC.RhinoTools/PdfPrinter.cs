using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;

using Rhino;
using BVTC.RhinoTools.Helpers;
using BVTC.osTools;

namespace BVTC.RhinoTools
{
    public class PdfPrinter
    {
        public static string CreatePDF(RhinoDoc doc, Rhino.Display.RhinoPageView pageView, double pageWidth, double pageHeight, int timer = 10)
        {
            // check for a suitable PDF printer //
            string printer = "";
            foreach (string p in osTools.PrinterTools.PdfPrinters())
            {
                if(osTools.PrinterTools.HasPaperSize(p, pageWidth, pageHeight, false))
                {
                    printer = p;
                    break;
                }
            }
            // throw and exception for invalid pdf printers //
            if (string.IsNullOrEmpty(printer))
            {
                throw new osTools.Exceptions.PrinterMissing(string.Format(
                    "Could not find suitable PDF printer, please install {0} and add a page size that is {1}x{2}", 
                    string.Join(", ",osTools.PrinterTools.PdfPrinters()), pageWidth, pageHeight));
            }

            // generate file destination //
            System.IO.FileInfo info = new System.IO.FileInfo(doc.Path);
            string name = info.Name.Substring(0, info.Name.LastIndexOf("."));
            string destination = info.DirectoryName + "\\" + info.Name + string.Format("_{0}x{1}.pdf", pageWidth, pageHeight);
            
            // create instance of pdf mover //
            osTools.FileShuffler shuffler = new osTools.FileShuffler(destination);

            // create file watcher to monitar the users desktop //
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            System.IO.FileSystemWatcher fileWatcher = new System.IO.FileSystemWatcher(desktop);
            fileWatcher.EnableRaisingEvents = true;

            // all setup is not complete, print the file //
            RhinoPrinter pdf_printer = new RhinoPrinter(doc, pageView, printer, pageHeight, pageWidth);

            // when a new file is created run the pdf shuffler //
            fileWatcher.Created += shuffler.OnFileSystemWatcherCreated;
            // add an error handler //
            fileWatcher.Error += pdf_printer.OnPrintError;
            
            pdf_printer.Print();

            // wait on main thread while pdf is getting shuffled around //
            DateTime end = DateTime.Now.AddSeconds(timer);
            while (shuffler.Moved == false)
            {
                RhinoApp.Wait();
                if (DateTime.Now > end) { break; }
            }
            if (shuffler.Moved == true)
            {
                return shuffler.finalDestination;
            }
            else
            {
                throw new Exceptions.File_Exception(string.Format(
                    "Unable to locate a pdf file in '{0}' please make sure {1} is configured to save files to the desktop, without showing prompt window.",
                    desktop, printer));
            }
        }

        public static List<string> UpdatePDFs(RhinoDoc doc, DataTable dt, string rhinoFiles = "", string pdfFiles = "")
        {
            List<string> updatedPDFs = new List<string>();
            /* Not used anymore 
            // make sure both columns were located //
            if (rhinoCol < 0 || pdfCol < 0)
            {
                throw new Exception(string.Format("Could not locate {0} & {1} in DataTable", rhinoFiles, pdfFiles));
            }

            foreach (DataRow row in dt.Rows)
            {
                string pdfPath = "";
                string rhinoPath = "";

                if (row[pdfCol].GetType() == typeof(string))
                {
                    pdfPath = (string)row[pdfCol];
                }
                if (row[rhinoCol].GetType() == typeof(string))
                {
                    rhinoPath = (string)row[rhinoCol];
                }
            }
            */
            return updatedPDFs;
        }

        public static string UpdatePDF(RhinoDoc doc, string rhinoPath, string pdfPath, osTools.PageSettings settings)
        {
            string path = "";

            try
            {
                // will throw an exception if rhinoPath is empty //
                if (!FileTools.IsFileUpToDate(rhinoPath, pdfPath))
                {
                    if (doc.Path != rhinoPath)
                    {
                        RhinoDoc.OpenFile(rhinoPath);
                        doc = RhinoDoc.ActiveDoc;
                        RhinoApp.Wait();
                    }

                    if (doc.Views.GetPageViews().Length > 0)
                    {
                        Rhino.Display.RhinoPageView pageView = doc.Views.GetPageViews()[0];
                        path = CreatePDF(doc, pageView, settings.PageWidth, settings.PageHeight);
                        Guid id = Document.GetGuid(doc, false);
                        if (!string.IsNullOrEmpty(path))
                        {
                            if (settings.PdfColumn == Collections.PdfColumn.ClientPDF)
                            {
                                new Repositories.CTrac().Update_ClientPDF(id, path);
                            }
                            else
                            {
                                new Repositories.CTrac().Update_ShopPDF(id, path);
                            }

                            pdfPath = path;
                        }
                    }
                    else
                    {
                        RhinoApp.WriteLine(string.Format(
                            "{0} has not layouts.", doc.Path));
                    }
                    doc.Modified = false;
                }
                else { path = pdfPath; }
            }
            catch (System.IO.FileNotFoundException e)
            {
                RhinoApp.WriteLine(string.Format(
                    "Unable to find file {0} skipping...", rhinoPath));
            }

            return path;
        }
    }
}
