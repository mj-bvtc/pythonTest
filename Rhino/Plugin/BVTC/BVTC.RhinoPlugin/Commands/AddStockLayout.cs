using System;
using Rhino;
using Rhino.Commands;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("0e4d40ad-0133-47bc-b642-7d494c772b5f")]
    public class AddStockLayout : Command
    {
        static AddStockLayout _instance;
        public AddStockLayout()
        {
            _instance = this;
        }

        ///<summary>The only instance of the AddStockLayout command.</summary>
        public static AddStockLayout Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "AddStockLayout"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // TODO: complete command.
            return Result.Success;
        }
    }
}
