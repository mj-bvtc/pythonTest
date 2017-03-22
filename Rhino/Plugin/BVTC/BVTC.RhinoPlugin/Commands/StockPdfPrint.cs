using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("02695768-be54-4bfd-9527-b54213a301b4"),
        CommandStyle(Style.ScriptRunner)]

    public class StockPdfPrint : Command
    {
        static StockPdfPrint _instance;
        public StockPdfPrint()
        {
            _instance = this;
        }

        ///<summary>The only instance of the StockPdfPrint command.</summary>
        public static StockPdfPrint Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "StockPdfPrint"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // get the active view //
            Rhino.Display.RhinoView view = doc.Views.ActiveView;
            if (view == null)
                return Rhino.Commands.Result.Failure;
            // check to make sure the current view is a layout //
            Rhino.Display.RhinoPageView pageView = view as Rhino.Display.RhinoPageView;
            if (pageView == null)
            {
                RhinoApp.WriteLine("Active viewport: '{0}' is not a layout", view.MainViewport.Name);
                return Rhino.Commands.Result.Failure;
            }

            // make sure the current document has a valid doc id //
            Guid id = Guid.Empty;
            if (RhinoTools.Document.HasGuid(doc))
            {
                id = RhinoTools.Document.GetGuid(doc, false);
            }
            else
            {
                RhinoApp.WriteLine("There is not document Guid assisgned to to this file.");
                return Result.Failure;
            }



            try
            {

                string shopPDF = RhinoTools.PdfPrinter.CreatePDF(doc, pageView, 11, 8.5);
                new Repositories.CTrac().Update_ShopPDF(id, shopPDF);
                RhinoApp.WriteLine(shopPDF);
            }
            catch (System.IO.IOException e)
            {
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                return Result.Failure;
            }
            catch (Exception e)
            {
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                return Result.Failure;
            }


            return Result.Success;
        }
    }
}
