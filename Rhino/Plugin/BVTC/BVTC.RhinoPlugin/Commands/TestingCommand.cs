using System;
using System.Collections.Generic;
using System.Linq;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;
using System.Data;
using System.Windows.Forms;

using BVTC.RhinoTools.Helpers;
using BVTC.Data.Helpers;
using BVTC.UI.Helpers;

namespace BVTC.RhinoPlugin
{
    [System.Runtime.InteropServices.Guid("bd393b94-5552-4808-b599-5d0c3a7595b9"),
        CommandStyle(Style.ScriptRunner)]
    public class TestingCommand : Command
    {
        public TestingCommand()
        {
            // Rhino only creates one instance of each command class defined in a
            // plug-in, so it is safe to store a refence in a static property.
            Instance = this;
        }

        ///<summary>The only instance of this command.</summary>
        public static TestingCommand Instance
        {
            get; private set;
        }

        ///<returns>The command name as it appears on the Rhino command line.</returns>
        public override string EnglishName
        {
            get { return "TestingCommand";  }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            return Result.Success;
        }
    }
}
