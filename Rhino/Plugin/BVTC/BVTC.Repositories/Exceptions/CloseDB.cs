using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Exceptions
{
    public class CloseDB : System.Exception
    {
        public CloseDB() : base()
        {
        }

        public CloseDB(string message)
        : base(message)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public CloseDB(string message, Exception inner)
        : base(message, inner)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }

        public CloseDB(database db)
        {
            System.Diagnostics.Debug.Write(Environment.StackTrace);
        }
    }
}
