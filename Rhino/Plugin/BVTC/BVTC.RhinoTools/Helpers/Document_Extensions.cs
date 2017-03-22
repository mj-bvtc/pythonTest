using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino;

namespace BVTC.RhinoTools.Helpers
{
    public static class Document_Extensions
    {
        public static bool LayoutExists(this RhinoDoc doc, string layoutName)
        {
            return doc.GetPageNames().Contains(layoutName);
        }

        public static string[] GetPageNames(this RhinoDoc doc)
        {
            // Return all page names from a RhinoDoc //
            Rhino.Display.RhinoPageView[] views = doc.Views.GetPageViews();
            string[] pageNames = new string[views.Length];
            for (int i = 0; i < views.Length; i++)
            {
                pageNames[i] = views[i].PageName;
            }
            return pageNames;
        }

    }
}
