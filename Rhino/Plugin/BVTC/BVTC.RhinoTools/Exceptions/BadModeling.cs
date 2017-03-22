using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace BVTC.RhinoTools.Exceptions
{
    public class BadModeling : Exception
    {
        public BadModeling() : base()
        {
        }

        public BadModeling(string message)
        : base(message)
        {
        }

        public BadModeling(string message, Exception inner)
        : base(message, inner)
        {
        }
    }
}
