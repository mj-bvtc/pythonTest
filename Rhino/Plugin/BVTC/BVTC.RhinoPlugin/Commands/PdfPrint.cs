using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("afab7ff5-dddd-4805-b54d-b64e0ffbf0ce"),
        CommandStyle(Style.ScriptRunner)]
    public class PdfPrint : Command
    {
        static PdfPrint _instance;
        public PdfPrint()
        {
            _instance = this;
        }

        ///<summary>The only instance of the PdfPrint command.</summary>
        public static PdfPrint Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "PdfPrint"; }
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
                RhinoApp.WriteLine("THere is not document Guid assisgned to to this file.");
                return Result.Failure;
            }

            List<string> layers = new Repositories.CTrac().Get_LayerNames("MoldShopComments", pageView.PageName);
            
            try
            {
                // turn on MS comments //
                //RhinoTools.Document.LayerVisible(doc, layers, true); doc.Views.Redraw();
                string shopPDF = RhinoTools.PdfPrinter.CreatePDF(doc, pageView, 11, 8.5);
                new Repositories.CTrac().Update_ShopPDF(id, shopPDF);
                osTools.PdfTools.RotatePDF(shopPDF);
                RhinoApp.WriteLine(shopPDF);

                // turn off MS comments //
                //RhinoTools.Document.LayerVisible(doc, layers, false); doc.Views.Redraw();
                string clientPDF = RhinoTools.PdfPrinter.CreatePDF(doc, pageView, 17, 11);
                new Repositories.CTrac().Update_ClientPDF(id, clientPDF);
                RhinoApp.WriteLine(clientPDF);
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
