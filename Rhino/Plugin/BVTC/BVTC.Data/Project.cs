using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data
{
    public class Project : data
    {
        public string name { get; set; }
        public string path { get; set; }
        public string dataFolder { get; set; }
        public string ShortDescription { get; set; }
        public string ProjectNumber { get; set; }
        public string pCode { get; set; }
    }

}
