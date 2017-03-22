using System;
using System.Linq;
using System.Collections.Generic;

using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

using BVTC.RhinoTools.Helpers;


namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("536aef14-8180-4e6f-ab0b-459e03350033")]
    public class RevTag : Command
    {
        static RevTag _instance;
        public RevTag()
        {
            _instance = this;
        }

        ///<summary>The only instance of the RevTag command.</summary>
        public static RevTag Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "RevTag"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            RhinoApp.WriteLine(this.EnglishName);

            // set current document in helper class //
            RhinoTools.Document currentDoc = new RhinoTools.Document(doc);

            // check that a layout is the active view //
            Rhino.Display.RhinoViewport active = doc.Views.ActiveView.ActiveViewport;
            

            if (doc.GetPageNames().Contains(active.Name) == false)
            {
                RhinoApp.WriteLine("Active View: {0} is not a page layout.", active.Name);
                return Result.Cancel;
            }

            // pull revistion data from C-Trac //
            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
            string rev = "";
            try
            {
                CTrac.OpenDB();
                rev = CTrac.CommandToString(
                string.Format("SELECT RevisionLetter('{0}')", RhinoTools.Document.GetGuid(doc, false)));
            }
            catch (Exception e)
            {
                throw e;
            }
            finally
            {
                CTrac.CloseDB();
            }

            if (rev == "")
            {
                RhinoApp.WriteLine("Unable to located a revision for file.");
                return Result.Cancel;
            }

            Point3d pt;
            double height = 0.125;
            Rhino.Display.Text3d text = new Rhino.Display.Text3d(rev, Plane.WorldXY, height);

            // live redraw of text object //
            using (GetPoint getPointAction = new GetPoint())
            {
                getPointAction.SetCommandPrompt("Place Text");
                getPointAction.DynamicDraw +=
                  (sender, e) => e.Display.Draw3dText(text, System.Drawing.Color.Red, e.CurrentPoint);

                if (getPointAction.Get() != GetResult.Point)
                {
                    RhinoApp.WriteLine("No end point was selected.");
                    return getPointAction.CommandResult();
                }
                pt = getPointAction.Point();
            }

            Plane plane = Plane.WorldXY;
            plane.Origin = pt;

            TextEntity textObj = new TextEntity();
            textObj.Text = rev;
            textObj.TextHeight = height;
            textObj.Plane = plane;

            // add object to document //
            Guid id = doc.Objects.AddText(textObj);
            if (id == Guid.Empty) { return Result.Failure; }

            Guid tri = RhinoTools.Geometry.BB_Triangle(doc, id);
            if (tri == Guid.Empty) { return Result.Failure; }

            string layer = "Revision::RevTag";

            // check if layer exists //
            if (RhinoTools.Document.IsLayer(doc, layer) == false)
                RhinoTools.Document.AddLayer(doc, layer);
            // add object to layer //
            RhinoTools.Document.Set_LayerByObject(doc, id, layer);
            RhinoTools.Document.Set_LayerByObject(doc, tri, layer);
            // set object color //
            RhinoTools.Document.Set_ColorByObject(doc, id, "Red");
            RhinoTools.Document.Set_ColorByObject(doc, tri, "Red");

            // group text and curves //
            doc.Groups.Add(new List<Guid>() { tri, id });

            doc.Views.Redraw();
            RhinoApp.WriteLine("{0} added to the document.", this.EnglishName);

            return Result.Success;
        }
    }
}
