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
    public class Part
    {
        public List<Guid> GuidList_Start { get; set; }
        public List<Guid> GuidList_OnXY { get; set; }
        public Guid KeyObject { get; set; }
        public BrepFace Bottom { get; set; }
        public double BottomIndex { get; set; }
        public double FrontIndex { get; set; }
        public Point3d BottomCentroid { get; set; }
        public BrepFace Front { get; set; }
        public Point3d FrontCentroid { get; set; }
        public Vector3d StartVec { get; set; }
        public Vector3d EndVec { get; set; }
        public List<Guid>GuidList_End { get; set; }
        public Plane BottomPlane { get; set; }
        public Plane XY = Plane.WorldXY;



    }
}



//new dataclass instance ---------> return dataclass instance [Part]

//select objects  -----------> return guids as list   [Part.GuidList_start]


//select key bottom face   ---------> return guid of object and guid of face on object  [Part.KeyObject, Part.Bottom]


//select key front face -------> return index of face on object  [Part.FrontIndex]


//remap bottom to XY  ------> return void


//calculate new bottom face centroid ------> return point3d  [Part.BottomCentroid]

//*******skip********calculate normal vector to bottom centroid --------> return vector3d



//identify new front face using new key object guid and front index ------> return guid  [Part.Front]

//identify centroid of newFrontFace ------->  return point3d [Part.FrontCentroid]

//create vector from bottomfacecentroid to newFrontFaceCentroid ------->return vector3d [Part.StartVector]

//project vector to XY plane (set z value to zero) ----->return vec3d [Part.EndVector]

//*******skip********calculate angle in radians between frontface vector and negYvector -------> return double

//*******skip********negate angleBetweenVectors -----> return double



//rotate [Part.GuidList]  to front using [Part.StartVector], [Part.EndVector], [Part.BottomCentroid] ----> return guid as list [Part.GuidList_end]