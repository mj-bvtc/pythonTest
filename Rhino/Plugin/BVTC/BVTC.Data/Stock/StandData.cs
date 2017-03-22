using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input.Custom;
using Rhino.DocObjects;
using System.Windows.Forms;
using Pervasive.Data.SqlClient;
using System.Text.RegularExpressions;
using System.CodeDom.Compiler;
using System.CodeDom;
using System.IO;
using System.Data;
using System.Reflection;
using System.Linq;
using System.Linq.Expressions;

namespace BVTC.Data.Stock
{
    public class Dimension
    {
        public int width;
        public int length;
        public int area;
        public bool isSquare;
        public bool wfits;
        public bool lfits;
        public bool standFits;
        public string name;
        public bool areaFits;

        public Dimension(int _width, int _length)
        {
            width = _width;
            length = _length;
            area = width * length;
            if (width == length) { isSquare = true; }
            else { isSquare = false; }
            name = string.Join("_", "Dim", width.ToString(), length.ToString());
        }
    }
        public class StandData : data
    {
        public double width { get; set; }
        public double length { get; set; }
        public Point3d pts { get; set; }
        public Brep block { get; set; }                     //set
        public BrepFace bottom { get; set; }                //set 
        public RhinoDoc doc { get; set; }                   //set before passing to stand class instance
        public double edge { get; set; }
        public int range { get; set; }
        public int step { get; set; }
        public Point3d centroid { get; set; }
        public BoundingBox box { get; set; }
        public bool areaFits { get; set; }
        public List<Dimension> dimList()
        {
            Dimension eighteenTwelve = new Dimension(18, 12);
            Dimension twelveEighteen = new Dimension(12, 18);
            Dimension sixTwelve = new Dimension(6, 12);
            Dimension twelveSix = new Dimension(12, 6);
            Dimension fiveFive = new Dimension(5, 5);
            List<Dimension> dim = new List<Dimension> { eighteenTwelve, twelveEighteen, sixTwelve, twelveSix, fiveFive };
            return dim;
        }

    }
}
