using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data.Exceptions
{
    public class BlockID_Exception : System.Exception
    {
        public BlockID_Exception() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public BlockID_Exception(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public BlockID_Exception(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
