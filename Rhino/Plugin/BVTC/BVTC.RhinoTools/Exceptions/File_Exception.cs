using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace BVTC.RhinoTools.Exceptions
{
    public class File_Exception : Exception
    {
        public File_Exception() : base()
        {
            Debug.Write(Environment.StackTrace);
        }

        public File_Exception(string message)
        : base(message)
        {
            Debug.Write(Environment.StackTrace);
        }

        public File_Exception(string message, Exception inner)
        : base(message, inner)
        {
            Debug.Write(Environment.StackTrace);
        }
    }
}
