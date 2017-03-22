using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Exceptions
{
    public class OpenDB : System.Exception
    {
        public OpenDB() : base()
        {
        }

        public OpenDB(string message)
        : base(message)
        {
        }

        public OpenDB(string message, Exception inner)
        : base(message, inner)
        {
        }

        public OpenDB(database db)
        {

        }
    }
}
