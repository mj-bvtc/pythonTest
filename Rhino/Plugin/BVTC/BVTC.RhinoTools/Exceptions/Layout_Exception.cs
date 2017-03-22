using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace BVTC.RhinoTools.Exceptions
{
    public class Layout_Exception : Exception
    {
        public Layout_Exception() : base()
        {
            Debug.Write(Environment.StackTrace);
        }

        public Layout_Exception(string message)
        : base(message)
        {
            Debug.Write(Environment.StackTrace);
        }

        public Layout_Exception(string message, Exception inner)
        : base(message, inner)
        {
            Debug.Write(Environment.StackTrace);
        }
    }
}
