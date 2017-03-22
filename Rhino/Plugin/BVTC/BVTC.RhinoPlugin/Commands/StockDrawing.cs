using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using System.IO;
using System.Linq;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("fe0ec87a-e09a-4621-8408-2b7b0439f707"), CommandStyle(Style.ScriptRunner)]
    public class StockDrawing : Command
    {
        static StockDrawing _instance;
        public StockDrawing()
        {
            _instance = this;
        }

        ///<summary>The only instance of the StockDrawing2 command.</summary>
        public static StockDrawing Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "StockDrawing"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            try
            {
                //save temp
                StockFunctions.SaveTemp(doc);

                //instantiate data classes
                Data.Stock.BrepData bd = new Data.Stock.BrepData();
                Data.Stock.StockData sd = new Data.Stock.StockData();

                //instantiate tools
                RhinoTools.Document rTools = new RhinoTools.Document(doc);

                //Delete old layouts
                RhinoTools.Layout.DeleteAllLayouts(doc);

                //Set display and show isocurves
                RhinoTools.Layout.Set_Viewport(doc, "Perspective");
                RhinoTools.Layout.Set_DisplayMode(doc, "Shaded");
                RhinoTools.Layout.ShowAllIsocurves(doc);
                RhinoTools.Layout.ZoomExtents(doc);

                //make selections
                string message = "Select objects to include in stock drawing";
                List<Guid> blockGuids = BVTC.RhinoTools.Document.GetObjects(doc, message);
                if(blockGuids.Count<1) { return Result.Cancel; }
                Data.Stock.Block getBottom = rTools.GetFace(doc);
                Data.Stock.Block getFront = rTools.GetFace(doc);


                //delete objects not in drawing
                List<Guid> everything = RhinoTools.Document.AllObjects(doc);
                List<Guid> stuffToDelete = everything.Except(blockGuids).ToList();
                doc.Objects.Delete(stuffToDelete, true);


                //set data
                Result setData = StockFunctions.SetData(doc, sd, bd, getBottom, getFront);
                if (setData != Result.Success) { return Result.Cancel; }

                //transform objects
                List<Guid> newObjs;
                var tup = StockFunctions.TransformObjects(doc, sd.Shrinkage, sd, bd, getBottom, getFront, blockGuids);
                newObjs = tup.Item1;
                NurbsCurve curve = tup.Item2;
             
                //MeasureStock          
                StockFunctions.MeasureStock(doc, newObjs, bd, curve);
                

                //transfer data
                sd.StockWidth = bd.width;
                sd.StockLength = bd.length;
                sd.StockHeight = bd.height;
                sd.Stock = string.Join(", ", sd.StockWidth.ToString(), sd.StockLength.ToString(), sd.StockHeight.ToString());
                if (string.IsNullOrWhiteSpace(bd.Stand) || bd.Stand == "0, 0" || bd.Stand == "0") 
                { sd.Stand = "Build Custom"; }
                else
                { sd.Stand = bd.Stand; }
                

                //Send data
                StockFunctions.SendData(doc, sd);


                //Silhouette Objects
                List<Guid> ids = RhinoTools.Document.AllObjects(doc);
                RhinoTools.Geometry.SilhouetteObjects(doc, ids);

                //Organize Layers
                StockFunctions.OrganizeLayers(doc, sd);

                //Make Layout
                StockFunctions.AddLayout(doc, sd, PlugIn);

                //save file
                RhinoTools.Document.SaveAs(doc, sd.ModelPath);

                return Result.Success;
            }
            catch(Exception e)
            {
                Rhino.RhinoApp.WriteLine(e.GetType().ToString());
                Rhino.UI.Dialogs.ShowMessageBox(e.Message, e.GetType().ToString());
                return Result.Cancel;
            }
           
        }
    }
}
