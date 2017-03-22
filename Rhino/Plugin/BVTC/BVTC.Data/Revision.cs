using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data
{
    class Revision : data
    {
        public string ProjectNumber { get; set; }
        public string BaseStyle { get; set; }
        public string guid { get; set; }
        public string Rev { get; set; }
        public string User { get; set; }
        public DateTime Date { get; set; }
        public int Count { get; set; }
        public string Description { get; set; }
    }
}
