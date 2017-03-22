using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Repositories
{
    class SQLCompact : database
    {
        public override void CloseDB()
        {
            throw new NotImplementedException();
        }

        public override DataTable CommandToDataTable(string cmdStr)
        {
            throw new NotImplementedException();
        }

        public override List<string> CommandToList(string cmdStr)
        {
            throw new NotImplementedException();
        }

        public override string CommandToString(string cmdStr)
        {
            throw new NotImplementedException();
        }

        public override int ExecuteCommand(string cmdStr)
        {
            throw new NotImplementedException();
        }

        public override List<string> GetColumnNames(string table)
        {
            throw new NotImplementedException();
        }

        public override void OpenDB()
        {
            throw new NotImplementedException();
        }
    }
}
