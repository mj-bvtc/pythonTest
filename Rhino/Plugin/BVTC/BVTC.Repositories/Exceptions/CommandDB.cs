using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories.Exceptions
{
    public class CommandDB : Exception
    {
        public CommandDB() : base()
        {
        }

        public CommandDB(string message)
        : base(message)
        {
        }

        public CommandDB(string message, Exception inner)
        : base(message, inner)
        {
        }

        public CommandDB(database db)
        {

        }
    }
}
