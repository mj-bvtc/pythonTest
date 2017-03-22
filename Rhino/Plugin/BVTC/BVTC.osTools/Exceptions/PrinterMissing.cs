using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.osTools.Exceptions
{
    public class PrinterMissing : System.Exception
    {
        public PrinterMissing() : base()
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public PrinterMissing(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public PrinterMissing(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
