using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Rhino.Geometry;


namespace BVTC.Data.Stock
{
    public class Block
    {
        public BrepFace face { get; set; }       
        public int faceIndex { get; set; }
        public Brep block { get; set; }
        public Guid blockGuid { get; set; }
        
        
    }
}
