using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Data;
using System.Diagnostics;

using Rhino;

using BVTC;
using BVTC.Repositories;
using BVTC.RhinoTools.Data;
using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoTools
{
    public class Layout
    {
        // constructors //
        public Layout(Rhino.Display.RhinoPageView view)
        {
            this.PageView = view;
            this.Doc = view.Document;
        }
        public Layout() { }

        // standard scale property //
        private List<double> standardScales = new List<double> { 1, 1.5, 3 };


        // properties //
        public RhinoDoc Doc { get; set; }
        public Rhino.Display.RhinoPageView PageView { get; set; }

        public static List<Guid> AddRevisionStamp(RhinoDoc doc, Rhino.Display.RhinoPageView pageView,
            string englishName, DataTable dt, double height = 0.147)
        {
            List<Guid> objs = new List<Guid>();

            // set input layout to current //
            doc.Views.ActiveView = pageView;

            for (int i = 0; i < dt.Rows.Count; i++)
            {
                List<RhinoText> textRow = new List<RhinoText>();
                for (int j = 0; j < dt.Columns.Count; j++)
                {
                    DataTable textProp = new CTrac().Get_TextInformation(
                        englishName, pageView.PageName, dt.Columns[j].ColumnName);

                    if (textProp.Rows.Count > 0)
                    {
                        // assign text properties from C-Trac //
                        RhinoText text = new RhinoText(textProp.Rows[0]);

                        // account for adding rows vertically //
                        string strText = dt.Rows[i][j].ToString();
                        text.y += height * (-i);

                        // create text object //
                        text.CreateText(doc, strText);
                        if (text.id != null)
                        {
                            objs.Add(text.id);
                        }
                    }
                }
            }

            return objs;
        }

        public static List<Guid> Build_RhinoTable(RhinoDoc doc, Rhino.Display.RhinoPageView layout,
            DataTable table, string command, double padding, bool clear)
        {
            // list to store ids just added to doc //
            List<Guid> ids = new List<Guid>();

            // set layout as current layout //
            Set_CurrentView(doc, layout.PageName);

            // clear old revision stamp text //
            List<string> layers = new CTrac().Get_LayerNames("table", layout.PageName);

            // delete layers if nessicary //
            if (clear)
            {
                foreach (string layer in layers)
                { Document.DeleteObjectsByLayer(doc, layer, layout); }
            }

            // get text info from ctrac //
            DataTable textProp = new CTrac().Get_TextInformation(command, layout.PageName, "table");

            RhinoTools.Data.RhinoText text;
            double totalWidth = 0;
            Rhino.Geometry.TextJustification forceJustify = Rhino.Geometry.TextJustification.TopLeft;

            for (int col = 0; col < table.Columns.Count; col++)
            {
                double width = 0;
                RhinoTools.Data.RhinoText[] list = new RhinoTools.Data.RhinoText[table.Rows.Count + 1];

                // add heading //
                text = new RhinoTools.Data.RhinoText(textProp.Rows[0]);
                list[0] = text;

                text.x = text.x + totalWidth;
                text.CreateText(doc, table.Columns[col].ColumnName, forceJustify);
                ids.Add(text.id);

                text.recHeight = text.textSize + padding;
                if (width < text.bb_X + padding)
                    width = text.bb_X + padding;


                // column text list //
                List<RhinoText> textCol = new List<RhinoText>();
                for (int row = 0; row < table.Rows.Count; row++)
                {
                    // create text object //
                    text = new RhinoTools.Data.RhinoText(textProp.Rows[0]);
                    list[row + 1] = text;

                    text.y = text.y - ((row + 1) * (text.textSize + padding));
                    text.x = text.x + totalWidth;

                    string value;
                    // have to convert all doubles to fractions if the unit system is standard //
                    // employees at Boston Valley Terra Cotta cannot read decimals with a ruler //
                    if (table.Rows[row][col].GetType() == typeof(double) &&
                        (doc.PageUnitSystem == UnitSystem.Inches || doc.PageUnitSystem == UnitSystem.Feet || doc.PageUnitSystem == UnitSystem.Yards))
                    {
                        double number = (double)table.Rows[row][col];
                        value = number.ToFraction();
                    }
                    else
                    {
                        value = table.Rows[row][col].ToString();
                    }

                    //RhinoApp.WriteLine(string.Format("{0}:'{1}' type:{2}", table.Columns[col].ColumnName, table.Rows[row][col], table.Rows[row][col].GetType()));
                    text.CreateText(doc, value, forceJustify);
                    //text.CreateText(doc, value);
                    ids.Add(text.id);

                    text.recHeight = text.textSize + padding;
                    if (width < text.bb_X + padding)
                        width = text.bb_X + padding;

                    textCol.Add(text);
                }
                totalWidth += width;
                // add rectangle //
                for (int row = 0; row < list.Length; row++)
                {
                    list[row].y += (padding / 2);
                    list[row].x -= (padding / 2);
                    list[row].recWidth = width;
                    ids.Add(list[row].CreateRectangle(doc, forceJustify));
                }

                // does not currently work as intended //
                // move text to proper justfication //
                foreach (RhinoText txt in textCol)
                {
                    Rhino.Geometry.TextJustification justify = (Rhino.Geometry.TextJustification)txt.justification;
                    Rhino.Geometry.Vector3d from = RhinoText.JustifyVector(forceJustify);
                    Rhino.Geometry.Vector3d to = RhinoText.JustifyVector(justify);
                    if (from - to != new Rhino.Geometry.Vector3d(0, 0, 0))
                    {
                        // calculate amount to move text to correct justification //
                        double x = (width - padding) * (to.X - from.X) - txt.bb_X * (to.X - from.X);
                        //double y = (height - padding) * (to.Y - from.Y) - txt.bb_Y * (to.Y - from.Y);
                        Rhino.Geometry.Vector3d move = new Rhino.Geometry.Vector3d(x, 0, 0);

                        Rhino.DocObjects.RhinoObject obj = doc.Objects.Find(txt.id);
                        if (obj != null && obj.GetType() == typeof(Rhino.DocObjects.TextObject))
                        {
                            Rhino.Geometry.TextEntity te = (Rhino.Geometry.TextEntity)obj.Geometry;
                            te.Translate(move);
                            doc.Objects.Replace(txt.id, te);
                        }
                        else
                        {
                            // couldn't find the id //
                        }
                    }
                }

            }

            /*
             * removed 11-7-16 
             * unable to fix layout - layer locking issue
             * issue was submitted to McNeel
            foreach (string layer in layers)
            {
                Document.LockLayer(doc, layer, true);
            }
            */

            // group all data for table //
            string groupName = string.Format("{0}_{1}_table", layout.PageName, command);
            Document.AddObjectsToGroup(doc, groupName, ids);

            return ids;

        }
        public static List<Guid> Build_RhinoTable(RhinoDoc doc, Rhino.Display.RhinoPageView layout, DataTable table, string command)
        {
            return Build_RhinoTable(doc, layout, table, command, .05, true);
        }
        public void Build_RhinoTable(DataTable table)
        {
            Build_RhinoTable(this.Doc, this.PageView, table, "Drawing", .05, true);

        }

        public static void Build_OversizeStamp(RhinoDoc doc, DataTable oversize, DataTable textInfo, double padding)
        {
            double height = 0;

            List<string> headings = oversize.GetHeadings();

            // Loop through all rows of oversize header //
            for (int i = 0; i < oversize.Rows.Count; i++)
            {
                // list of text classes //
                List<RhinoText> textRow = new List<RhinoText>();

                double rowHeight = 0;
                for (int j = 0; j < oversize.Columns.Count; j++)
                {
                    // assign text properties from C-Trac //
                    RhinoText text = new RhinoText(textInfo.Rows[j]);

                    // account for adding rows vertically //
                    string strText = oversize.Rows[i][j].ToString();
                    text.y += height + padding;
                    if (strText != null)
                    {
                        if (strText == "0") { strText = ""; }

                        text.CreateText(doc, strText);

                        if (text.recWidth != null && text.recWidth != 0)
                        {
                            // measure height of text to place next objects accordingly //
                            double size = 0;
                            if (text.id != Guid.Empty)
                            {
                                size = Geometry.Get_BoundingBox(doc, text.id, text.plane).Measure_Y();
                            }
                            if (size > rowHeight) { rowHeight = size; }
                        }
                    }

                    // add text class to list //
                    textRow.Add(text);
                }
                // account for text padding constant //
                rowHeight += 2 * padding;

                // add rectangles //
                foreach (RhinoText text in textRow)
                {
                    text.y -= padding;
                    text.recHeight = rowHeight;
                    Guid id = text.CreateRectangle(doc);
                }
                height += rowHeight;
            }

            // add heading text to layout //
            for (int i = 0; i < headings.Count; i++)
            {
                RhinoText text = new RhinoText(textInfo.Rows[i]);
                text.y += height + padding;

                // don't add suffix to column names //
                text.suffix = "";

                text.text = headings[i];
                text.CreateText(doc);
            }

            doc.Views.Redraw();
        }

        public static void LockAllDetails(RhinoDoc doc, Rhino.Display.RhinoPageView layout, bool locked)
        {
            layout.SetPageAsActive();
            doc.Views.ActiveView = layout;
            foreach (Rhino.DocObjects.DetailViewObject detail in layout.GetDetailViews())
            {
                // lock each detail in a loop //
                layout.SetActiveDetail(detail.Id);
                detail.DetailGeometry.IsProjectionLocked = locked; // should be changed to locked //
                detail.CommitChanges();
                detail.CommitViewportChanges();
            }
            layout.SetPageAsActive();
            doc.Views.ActiveView = layout;
            doc.Views.Redraw();

        }
        public void LockAllDetails()
        {
            /* Over loaded function to use stored data in class.
             */
            LockAllDetails(this.Doc, this.PageView, true);
        }

        // run once detail is active //
        public static void HideInDetail(RhinoDoc doc, Rhino.DocObjects.DetailViewObject detail, List<Guid> ids)
        {

            RhinoApp.RunScript("-_ShowInDetail ", false);

            string cmd = "-_HideInDetail ";
            foreach (Guid id in ids)
            {
                cmd += "_SelID ";
                cmd += id.ToString() + " ";
            }
            cmd += "_Enter ";
            RhinoApp.RunScript(cmd, false);
        }

        public static Rhino.Display.RhinoPageView Set_CurrentView(RhinoDoc doc, string viewName)
        {
            // loop through doc page layouts //
            foreach (Rhino.Display.RhinoPageView view in doc.Views.GetPageViews())
            {
                if (view.PageName == viewName)
                {
                    doc.Views.ActiveView = view;
                    return view;
                }
            }

            // show error message //
            throw new Exceptions.Layout_Exception(
                string.Format("Layout: '{0}' does not exist in current document.", viewName));
        }
        public bool Set_CurrentView()
        {
            if (this.Doc == null)
            {
                throw new Exception("A Rhino.PageView was not set within the Layout class");
            }
            this.Doc.Views.ActiveView = this.PageView;
            return true;
        }

        public static void TitleBlockText(RhinoDoc doc, BVTC.Data.data data, Rhino.Display.RhinoPageView layout, string englishName, bool clear)
        {
            // set layout to current layout //
            Set_CurrentView(doc, layout.PageName);

            List<string> layers = new CTrac().Get_LayerNames(englishName, layout.PageName);

            // delete layers if nessicary //
            if (clear)
            {
                foreach (string layer in layers)
                {
                    Document.LockLayer(doc, layer, false);
                    Document.DeleteObjectsByLayer(doc, layer, layout);
                }
            }

            // text layout info from C-Trac into DataTable //
            DataTable textProperties = new CTrac().Get_TextInformation(englishName, layout.PageName);

            // loop through all data //
            for (int i = 0; i < textProperties.Rows.Count; i++)
            {
                // assign text properties from C-Trac //
                BVTC.RhinoTools.Data.RhinoText text = new RhinoText(textProperties.Rows[i]);
                PropertyInfo prop = data.GetType().GetProperty(text.className);
                if (prop != null)
                {
                    var value = prop.GetValue(data, null);
                    if (value != null)
                    {
                        text.CreateText(doc, data.OutputString(text.className));
                    }
                    else
                    {
                        RhinoApp.WriteLine("value of :" + text.className + " is null.");
                    }
                }
                else
                    RhinoApp.WriteLine(text.className + " does not exist in this class.");
            }
            /* reomved 11-17-16
             * issues with locking layers on layout
            foreach (string layer in layers)
            {
                Document.LockLayer(doc, layer, true);
            }
            */

            doc.Views.Redraw();
        }

        // zoom helper functions //
        private static void ZoomExtents_Details(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids)
        {
            // make layout active view //
            doc.Views.ActiveView = layout;
            layout.Redraw();

            // pull details from layout page //
            Rhino.DocObjects.DetailViewObject[] details = layout.GetDetailViews();
            foreach (Rhino.DocObjects.DetailViewObject detail in details)
            {
                // set detail as active //
                layout.SetActiveDetail(detail.Id);

                // make sure detail is not locked //
                if (detail.DetailGeometry.IsProjectionLocked == true)
                {
                    detail.DetailGeometry.IsProjectionLocked = false;
                    detail.CommitChanges();
                }

                // hide objects that are not to be included in detail views //
                if (ids.Count > 0)
                {
                    HideInDetail(doc, detail, ids);
                }
            }

            // THIS IS NESSICARY //
            foreach (Rhino.DocObjects.DetailViewObject detail in details)
            {
                // set detail as active //
                layout.SetActiveDetail(detail.Id);
                // zoom extents & commit the changes to the doc //
                if (detail.Viewport.ZoomExtents())
                {
                    detail.CommitViewportChanges();
                }
                else
                {
                    RhinoApp.WriteLine("Unable to ZE!!!");
                }

                // will not work without flush & redraw each time //
                RhinoApp.Wait();
                layout.Redraw();

            }
            // set active page back to main layout //
            layout.SetPageAsActive();
            layout.Redraw();
        }
        private void ZoomExtents_Details(List<Guid> ids)
        {
            ZoomExtents_Details(this.Doc, this.PageView, ids);
        }
        private static double calc_zoomMin(Rhino.Display.RhinoPageView layout, double padding = 0.9)
        {
            List<double> scales = new List<double>();
            // pull details from layout page //
            foreach (Rhino.DocObjects.DetailViewObject detail in layout.GetDetailViews())
            {
                if (detail.DetailGeometry.PageToModelRatio > 0)
                {
                    // get model scale //
                    scales.Add(detail.DetailGeometry.PageToModelRatio);
                }

            }
            // get min zoomed view for details //
            double min = scales.Min() * padding;

            // assign default value for scales //
            double scale = min;

            return min;
        }
        private static double calc_zoomStandard(Rhino.Display.RhinoPageView layout, List<double> standardScales, double padding = 0.9)
        {
            // get min of current layouts //
            double min = calc_zoomMin(layout, padding);

            // set scale equal to min if model is too large for all standard scales //
            double scale = min;

            // check all scales against 
            foreach (double value in standardScales)
            {
                if ((value / 12) <= min)
                {
                    scale = (value / 12);
                }
            }

            // return best fitting standard scale //
            return scale;
        }
        private static bool zoomAllDetails(RhinoDoc doc, Rhino.Display.RhinoPageView layout, double scale)
        {
            bool result = true;

            // get unit systems //
            UnitSystem model_units = doc.ModelUnitSystem;
            UnitSystem page_units = doc.PageUnitSystem;

            // change scale of all details //
            foreach (Rhino.DocObjects.DetailViewObject detail in layout.GetDetailViews())
            {
                if (detail.DetailGeometry.SetScale(1, model_units, scale, page_units))
                {
                    detail.CommitChanges();
                }
                else
                {
                    result = false;
                }
            }

            // set page as active //
            layout.SetPageAsActive();
            layout.Redraw();

            return result;
        }

        private static bool zoomStandard(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids, List<double> standardScales, double padding = 0.9)
        {
            // zoom extents for all views //
            ZoomExtents_Details(doc, layout, ids);

            // get closest standard scale //
            double scale = calc_zoomStandard(layout, standardScales, padding);

            // return true if scale was set for all details //
            return zoomAllDetails(doc, layout, scale);
        }
        private static bool zoomMaximum(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids, double padding = 0.9)
        {
            // zoom extents for all views //
            ZoomExtents_Details(doc, layout, ids);

            // calculate minimum across details //
            double scale = calc_zoomMin(layout, padding);

            // return true if scale was set for all details //
            return zoomAllDetails(doc, layout, scale);
        }
        private static bool zoomCustom(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids, double scale)
        {
            // zoom extents for all views //
            ZoomExtents_Details(doc, layout, ids);

            // return true if scale was set for all details //
            return zoomAllDetails(doc, layout, scale);
        }

        public static void ZoomDetails(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids, string mode = "Auto", double scale = 0)
        {
            if (mode == "Auto")
            {
                double padding = 0.9;   // percent of window to occupy

                // create a list of standard scales to use //
                List<double> standardScales = new List<double>();
                standardScales.Add(1);     // 1" = 1'-0"
                standardScales.Add(1.5);   // 1-1/2" = 1'-0"   
                standardScales.Add(3);     // 3" = 1'-0"

                zoomStandard(doc, layout, ids, standardScales, padding);
            }

            if (mode == "Maximum")
            {
                double padding = 0.9;   // percent of window to occupy
                zoomMaximum(doc, layout, ids, padding);
            }

            if (mode == "Custom" && scale > 0)
            {
                zoomCustom(doc, layout, ids, scale);
            }
        }


        public static void Set_DisplayMode(RhinoDoc doc, string modeName)
        {
            Rhino.Display.DisplayModeDescription mode = Rhino.Display.DisplayModeDescription.FindByName(modeName);
            doc.Views.ActiveView.ActiveViewport.DisplayMode = mode;
            doc.Views.Redraw();
        }

        public static void ZoomExtents(RhinoDoc doc)
        {
            doc.Views.ActiveView.ActiveViewport.ZoomExtents();
        }

        public static void DeleteAllLayouts(RhinoDoc doc)
        {
            Rhino.Display.RhinoPageView[] pageviews = doc.Views.GetPageViews();
            foreach (var page in pageviews)
            {
                page.Close();
            }

        }

        public static void ShowAllIsocurves(RhinoDoc doc)
        {
            foreach (var obj in doc.Objects)
            {
                if (obj.Geometry.HasBrepForm)
                {
                    if (obj.Attributes.WireDensity < 0)
                    {
                        obj.Attributes.WireDensity = 2;
                        obj.CommitChanges();
                    }

                }

            }

            doc.Views.Redraw();
        }


        public static void Set_Viewport(RhinoDoc doc, string viewname)
        {
            Rhino.Display.RhinoView[] views = doc.Views.GetViewList(true, false);
            foreach (var item in views)
            {
                if (item.MainViewport.Name == viewname)
                {
                    doc.Views.ActiveView = item;
                    item.Maximized = true;
                }
            }


            doc.Views.Redraw();

        }


        public static void Details_ZoomExtents(RhinoDoc doc, Rhino.Display.RhinoPageView layout, List<Guid> ids)
        {
            // make layout active view //
            doc.Views.ActiveView = layout;

            // pull details from layout page //
            Rhino.DocObjects.DetailViewObject[] details = layout.GetDetailViews();
            foreach (Rhino.DocObjects.DetailViewObject detail in details)
            {
                // make sure detail is not locked //
                if (detail.DetailGeometry.IsProjectionLocked == true)
                {
                    detail.DetailGeometry.IsProjectionLocked = false;
                    detail.CommitChanges();
                }
                // set detail as active //
                layout.SetActiveDetail(detail.Id);

                // hide objects that are not to be included in detail views //
                if (ids.Count > 0) { HideInDetail(doc, detail, ids); }

                // zoom extents & commit the changes to the doc //
                detail.Viewport.ZoomExtents();
                detail.CommitViewportChanges();

                // will not work without flush & redraw each time //
                RhinoApp.Wait();

            }
            // set active page back to main layout //
            layout.SetPageAsActive();
            layout.Redraw();
        }
        public static void Details_ZoomExtents(RhinoDoc doc, Rhino.Display.RhinoPageView layout)
        {
            // make layout active view //
            doc.Views.ActiveView = layout;

            // pull details from layout page //
            Rhino.DocObjects.DetailViewObject[] details = layout.GetDetailViews();
            foreach (Rhino.DocObjects.DetailViewObject detail in details)
            {
                // make sure detail is not locked //
                if (detail.DetailGeometry.IsProjectionLocked == true)
                {
                    detail.DetailGeometry.IsProjectionLocked = false;
                    detail.CommitChanges();
                }
                // set detail as active //
                layout.SetActiveDetail(detail.Id);

                // zoom extents & commit the changes to the doc //
                detail.Viewport.ZoomExtents();
                detail.CommitViewportChanges();

                // will not work without flush & redraw each time //
                RhinoApp.Wait();
                doc.Views.Redraw();

            }
            // set active page back to main layout //
            layout.SetPageAsActive();
            layout.Redraw();
        }
        public void Details_ZoomExtents(List<Guid> ids)
        {
            Details_ZoomExtents(this.Doc, this.PageView, ids);
        }

        public static void Details_ZoomByFactor(RhinoDoc doc, Rhino.Display.RhinoPageView layout, double zoomFactor)
        {
            // make layout active view //
            doc.Views.ActiveView = layout;

            // pull details from layout page //
            Rhino.DocObjects.DetailViewObject[] details = layout.GetDetailViews();
            foreach (Rhino.DocObjects.DetailViewObject detail in details)
            {
                // make sure detail is not locked //
                if (detail.DetailGeometry.IsProjectionLocked == true)
                {
                    detail.DetailGeometry.IsProjectionLocked = false;
                    detail.CommitChanges();
                }
                // set detail as active //
                layout.SetActiveDetail(detail.Id);

                // zoom extents & commit the changes to the doc //
                detail.Viewport.Magnify(zoomFactor, false);
                detail.CommitViewportChanges();

                // will not work without flush & redraw each time //
                RhinoApp.Wait();

            }
            // set active page back to main layout //
            layout.SetPageAsActive();
            layout.Redraw();
        }








        public static void PrintPDF(RhinoDoc doc, Rhino.Display.RhinoPageView pageView, string printer)
        {
            BVTC.RhinoTools.Layout.Set_CurrentView(doc, pageView.PageName);

            // get printer list //
            if (BVTC.osTools.PrinterTools.GetPrinters().Contains(printer))
            {
                // print rhino layout as PDF //
                string cmd = "_-Print " +
                    "_Setup _Destination " +
                    "_Printer " +
                    '"' + printer + '"' +
                    " _Enter _Enter _Go";

                RhinoApp.RunScript(cmd, true);
            }
            else
            {
                RhinoApp.WriteLine(string.Format("printer '{0}' is not installed.", printer));
            }

        }
    }
}