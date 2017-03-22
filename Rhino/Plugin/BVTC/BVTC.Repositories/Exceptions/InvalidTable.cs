using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Exceptions
{
    class InvalidTable : Exception
    {
        public InvalidTable() : base()
        {
        }

        public InvalidTable(string message)
        : base(message)
        {
        }

        public InvalidTable(string message, Exception inner)
        : base(message, inner)
        {
        }

        public InvalidTable(database db)
        {

        }
    }
}
