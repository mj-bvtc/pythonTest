using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.osTools.Exceptions
{
    public class FileInUse : System.Exception
    {
        public FileInUse() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public FileInUse(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public FileInUse(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
