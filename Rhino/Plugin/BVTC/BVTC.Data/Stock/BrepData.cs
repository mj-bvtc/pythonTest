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
    public class BrepData : data
    {
        public BrepFace bottom { get; set; }
        public BrepFace front { get; set; }
        public int frontIndex { get; set; }
        public Brep block { get; set; }
        public List<Guid> blockGuids { get; set; }
        public BrepFace newBottom { get; set; }
        public int botIndex { get; set; }
        public int length { get; set; }
        public int width { get; set; }
        public int height { get; set; }
        public string Stand { get; set; }
    }
}
