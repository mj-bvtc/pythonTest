using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data.Exceptions
{
    public class DataMisMatch_Exception : System.Exception
    {
        public DataMisMatch_Exception() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public DataMisMatch_Exception(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public DataMisMatch_Exception(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
