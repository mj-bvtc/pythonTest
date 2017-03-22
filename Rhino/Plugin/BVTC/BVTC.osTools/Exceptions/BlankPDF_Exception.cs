using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace BVTC.osTools.Exceptions
{
    public class BlankPDF_Exception : Exception
    {
        public BlankPDF_Exception() : base()
        {
            Debug.Write(Environment.StackTrace);
        }

        public BlankPDF_Exception(string message)
        : base(message)
        {
            Debug.Write(Environment.StackTrace);
        }

        public BlankPDF_Exception(string message, Exception inner)
        : base(message, inner)
        {
            Debug.Write(Environment.StackTrace);
        }
    }
}
