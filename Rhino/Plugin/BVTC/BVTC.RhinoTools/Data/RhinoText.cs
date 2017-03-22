using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using Rhino;
using Rhino.Geometry;

using BVTC.Data;
using BVTC.RhinoTools.Helpers;

namespace BVTC.RhinoTools.Data
{
    public class RhinoText : data
    {
        public RhinoText() : base() { }
        public RhinoText(DataRow row) : base(row) { }
        public RhinoText(data d) : base(d){ }

        public string className { get; set; }

        public string text { get; set; }
        public double x { get; set; }
        public double y { get; set; }
        public double z { get; set; }
        public double autoX { get; set; }
        public double autoY { get; set; }
        public double textSize { get; set; }
        public int justification { get; set; }
        public string suffix { get; set; }
        public int charsPerLine { get; set; }
        public double recWidth { get; set; }
        public double recHeight { get; set; }
        public string color { get; set; }
        public string layer { get; set; }

        // text info to be populated once object created //
        public Guid id { get; set; }
        public double bb_X { get; set; }
        public double bb_Y { get; set; }


        public Plane plane { get; set; }

        private void createPlane()
        {
            // create plane for text //
            Point3d pt = new Point3d(this.x, this.y, this.z);
            Vector3d normal = new Vector3d(0, 0, 1);
            this.plane = new Plane(pt, normal);
        }

        public string FormatText(string str)
        {
            string newString = "";
            while (str.Length >= this.charsPerLine)
            {

                int index = str.Substring(0, this.charsPerLine).LastIndexOf(' ');
                if (index > 0)
                {
                    // try to split string on spaces.
                    newString += str.Substring(0, index) + "\n";
                    str = str.Substring(index, str.Length - index);
                }
                else
                {
                    // otherwise split string with dashes to seperate.
                    newString += str.Substring(0, this.charsPerLine - 1) + "-\n";
                    str = str.Substring(this.charsPerLine - 1, str.Length - this.charsPerLine + 1);
                }
                str = str.TrimStart();
            }
            newString += str;
            return newString;
        }

        public void CreateText(RhinoDoc doc, bool organize)
        {
            // empty text entity //
            TextEntity text = new TextEntity();

            // make sure there is text to add //
            if (this.text == string.Empty) { return; }

            // add suffix charectors //
            if (this.suffix != "" && this.text != "")
                this.text += suffix;

            // format text into multiple lines //
            if (this.charsPerLine > 0)
                this.text = FormatText(this.text);

            // set text justification
            if (this.justification > 0)
            {
                var just = Enum.ToObject(typeof(Rhino.Geometry.TextJustification), this.justification);
                text.Justification = (Rhino.Geometry.TextJustification)just;
            }
            // create plane //
            this.createPlane();

            // setup text properties //
            text.Text = this.text;
            text.TextHeight = this.textSize;
            text.Plane = this.plane;

            // add text object //
            Guid guid = doc.Objects.AddText(text);

            // organize text //
            if (organize == true)
                OrganizeText(doc, guid);

            // measure text size //
            this.id = guid;
            BoundingBox bb = Geometry.Get_BoundingBox(doc, id, this.plane);
            this.bb_X = bb.Measure_X();
            this.bb_Y = bb.Measure_Y();

            // scale text to be correct size //
            if (autoX > 0 && autoX < this.bb_X)
            {
                this.textSize = this.textSize * autoX / this.bb_X;
                text.TextHeight = this.textSize;
                doc.Objects.Replace(guid, text);

                // resize bounding box //
                bb = Geometry.Get_BoundingBox(doc, id, this.plane);
                this.bb_X = bb.Measure_X();
                this.bb_Y = bb.Measure_Y();
            }
            if (autoY > 0 && autoY < this.bb_Y)
            {
                this.textSize = 
                text.TextHeight = this.textSize * autoY / this.bb_Y;
                doc.Objects.Replace(guid, text);

                //resize bounding box //
                bb = Geometry.Get_BoundingBox(doc, id, this.plane);
                this.bb_X = bb.Measure_X();
                this.bb_Y = bb.Measure_Y();
            }

        }
        public void CreateText(RhinoDoc doc, string text)
        {
            // over loaded class for adding text //
            this.text = text;
            CreateText(doc, true);
        }
        public void CreateText(RhinoDoc doc, string text, bool organize)
        {
            CreateText(doc, organize);
        }
        public void CreateText(RhinoDoc doc)
        {
            CreateText(doc, true);
        }
        public void CreateText(RhinoDoc doc, string text, int forceJustify)
        {
            this.text = text;
            // store justify setting and reapply //
            int justify = this.justification;
            this.justification = forceJustify;
            CreateText(doc, true);
            this.justification = justify;

        }
        public void CreateText(RhinoDoc doc, string text, TextJustification forceJustify)
        {
            int j = (int)forceJustify;
            CreateText(doc, text, j);
        }


        public Guid CreateRectangle(RhinoDoc doc, bool organize = true)
        {
            Guid id = new Guid();
            if (this.recHeight > 0 && this.recWidth > 0)
            {
                // regenerate new base plane //
                this.createPlane();

                // set correct location for point based on justification //
                Point3d basePt = new Point3d(this.plane.OriginX, this.plane.OriginY, this.plane.OriginZ);

                // move horizontal //
                int horizontal = (this.justification % 65536) / 2;
                Vector3d axis = new Vector3d(this.plane.XAxis);
                Transform xform = Transform.Translation(axis * horizontal / -2 * this.recWidth);
                basePt.Transform(xform);

                // move vertical //
                int vertical = (this.justification / 65536) / 2;
                axis = new Vector3d(this.plane.YAxis);
                xform = Transform.Translation(axis * vertical / -2 * this.recHeight);
                
                basePt.Transform(xform);

                // create new relocated plane //
                Plane recPlane = new Plane(basePt, this.plane.Normal);

                Rectangle3d rec = new Rectangle3d(recPlane, this.recWidth, this.recHeight);
                Polyline poly = rec.ToPolyline();
                id = doc.Objects.AddPolyline(poly);

                // organize objects on layer //
                if (organize == true)
                    OrganizeText(doc, id);

            }
            else
                // these need to get converted to Exceptions //
                RhinoApp.WriteLine("Missing rectangle height and width.");
            return id;
        }
        public Guid CreateRectangle(RhinoDoc doc, int justification)
        {
            int prev = this.justification;
            this.justification = justification;
            Guid id = CreateRectangle(doc);
            this.justification = prev;
            return id;
        }
        public Guid CreateRectangle(RhinoDoc doc, Rhino.Geometry.TextJustification justify)
        {
            int j = (int)justify;
            return CreateRectangle(doc, j);
        }

        public double MeasureTextWidth(System.Guid id)
        {

            double size = 0;
            if (id != Guid.Empty)
            {


                /*
                Point3d pt = bb.Corner(true, true, true);
                size = pt.DistanceTo(bb.Corner(false, true, true));
                */

            }
            else { RhinoApp.WriteLine("text object has not yet been created."); }
            return size;
        }

        public void OrganizeText(RhinoDoc doc, Guid id)
        {
            if (this.layer != null && this.layer != "")
            {
                // check if layer exists //
                if (Document.IsLayer(doc, this.layer) == false)
                    Document.AddLayer(doc, this.layer);
                // add object to layer //
                Document.Set_LayerByObject(doc, id, this.layer);
            }
            else
                RhinoApp.WriteLine("<text.layer> was not specified in class");

            // set object color //
            if (this.color != null && this.color != "")
                Document.Set_ColorByObject(doc, id, this.color);
            else
                RhinoApp.WriteLine("<text.color> was not specified in class");
        }

        public static Vector3d JustifyVector(TextJustification justify)
        {
            /* Value  Description
            *  1      Left
            *  2      Center (horizontal)
            *  4      Right
            *  65536  Bottom
            *  131072 Middle (vertical)
            *  262144 Top
            */
            int j = (int)justify;

            double horizontal = (j % 65536) / 2;
            double vertical = (j / 65536) / 2;

            return new Vector3d(horizontal / 2, vertical / 2, 0);
        }
    }
}
