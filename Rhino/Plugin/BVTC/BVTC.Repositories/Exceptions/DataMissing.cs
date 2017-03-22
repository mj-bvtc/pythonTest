using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Exceptions
{
    public class DataMissing : System.Exception
    { 
       
        public DataMissing() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public DataMissing(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public DataMissing(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

    }
}
