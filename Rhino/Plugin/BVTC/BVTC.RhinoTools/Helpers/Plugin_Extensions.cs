using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.IO;
using Rhino;

namespace BVTC.RhinoTools.Helpers
{
    public static class Plugin_Extensions
    {
        public static string GetPluginFolder(this Rhino.PlugIns.PlugIn plugin)
        {
            foreach (string folder in Rhino.PlugIns.PlugIn.GetInstalledPlugInFolders())
            {
                string path = Rhino.PlugIns.PlugIn.PathFromId(plugin.Id);
                if (FileStructure.IsFileInFolder(path, folder) == true)
                {
                    return folder;
                }
            }

            // plugin ID could nob be found in Rhino Docuemnt //
            return null;
        }

        public static string GetBaseFolder(this Rhino.PlugIns.PlugIn plugin)
        {
            DirectoryInfo info = new DirectoryInfo(plugin.GetPluginFolder());
            return info.Parent.Parent.FullName;
        }
    }
}
