using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.RhinoTools.Exceptions
{
    public class MissingGUID_Exception : System.Exception
    {
        public MissingGUID_Exception() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public MissingGUID_Exception(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public MissingGUID_Exception(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
