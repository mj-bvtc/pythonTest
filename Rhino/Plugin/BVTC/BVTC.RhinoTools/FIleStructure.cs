using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

using Rhino;
using BVTC.RhinoTools.Helpers;
using BVTC.Data.Helpers;

namespace BVTC.RhinoTools
{
    /// <summary>
    /// FileStructure:
    ///     Methods specific to Boston Valley Terra Cotta's
    ///     organizational folder structure.
    ///     
    /// Methods:
    ///     Find_Template - locates path of 3dm template file.
    /// </summary>
    public class FileStructure
    {
        public static string Find_DataFolder(RhinoDoc doc)
        {
            string dataFolder = "";
            string df = "_Data";
            int index;
            List<string> folders = new List<string>();

            List<string> splits = doc.Path.Split('\\').ToList<string>();

            if (splits.Contains("TerraCotta") == true)
            {
                index = splits.IndexOf("TerraCotta");
                folders = splits.GetRange(0, index + 1);
            }
            else if (splits.Contains("CNC") == true)
            {
                index = splits.IndexOf("CNC");
                folders = splits.GetRange(0, index + 1);
            }
            else if (splits.Contains("Drawings") == true)
            {
                index = splits.IndexOf("Drawings");
                folders = splits.GetRange(0, index + 1);
            }
            else if (splits.Contains("Projects") == true)
            {
                index = splits.IndexOf("Projects");
                folders = splits.GetRange(0, index + 2);
                folders.Add("TerraCotta");
            }

            folders.Add(df);
            dataFolder = string.Join("\\", folders) + "\\";
            Directory.CreateDirectory(dataFolder);

            return dataFolder;
        }

        public static string Find_File(Rhino.PlugIns.PlugIn plugin, string fileName)
        {

            string extension = '.' + fileName.Split('.')[fileName.Split('.').Length - 1];
            string baseFolder = plugin.GetBaseFolder();

            // generate correct folder location //
            string path = baseFolder + @"\BVTC.RhinoPlugin\Templates" + extension + @"\" + fileName;

            // check to make sure path exisists //
            if (File.Exists(path) == true) { return path; }
            else
            {
                throw new Exceptions.File_Exception(string.Format("Could not find file {0}", path));
            }

            
        }
        public static string Find_Template(Rhino.PlugIns.PlugIn plugin)
        {
            return Find_File(plugin, "Synch_Drawings.3dm");
        }

        public static string Find_ProjectFolder(RhinoDoc doc)
        {
            /* Find the actual location of the project folder for input document
             * This will not nessicarily match what the project is named in C-Trac
             * Retruns - string path of project folder
             */
            string folder = "";
            List<string> splits = doc.Path.Split('\\').ToList<string>();
            // Find location for /Project folder 
            if (splits.Contains("Projects") == true)
            {
                int index = splits.IndexOf("Projects");
                folder = string.Join<string>("\\", splits.GetRange(0, index + 2));
            }
            else { RhinoApp.WriteLine(string.Format(@"File {0} must be saved into a job in the \Projects\ folder", doc.Path)); }

            return folder;
        }

        public static string Find_ProjectName(RhinoDoc doc)
        {
            /* Return the Project Name String
             * This will find the name of the folder the file is saved to.
             * IE - V:/Projects/Woolworth Building/Terracotta/S1R/S1R.3dm -> "Woolworth Building"
             */
            string projectName = "";
            if (doc.Name == "") { RhinoApp.RunScript("!Save", true); }
            if (doc.Name == "") { RhinoApp.WriteLine("Failed to save file..."); return projectName; }
            List<string> splits = doc.Path.Split('\\').ToList<string>();

            // Find location for /Project folder 
            if (splits.Contains("Projects") == true)
            {
                int index = splits.IndexOf("Projects");
                projectName = splits[index + 1];
            }
            else { RhinoApp.WriteLine(@"The current file must be saved into a job in the \Projects\ folder"); }
            return projectName;
        }

        public static bool IsFileInFolder(string file, string folder)
        {
            /* Check to see if a file is nested in a folder
             */

            string[] fileSplit = file.Split('\\');
            string[] folderSplit = folder.Split('\\');

            for (int i = 0; i < folderSplit.Length; i++)
            {
                if (folderSplit[i] != fileSplit[i])
                {
                    return false;
                }
            }
            return true;
        }

        public static void WalkDirectoryTree(System.IO.DirectoryInfo root, 
            List<System.IO.FileInfo> results, string extension = "*")
        {
            System.IO.FileInfo[] files = null;
            System.IO.DirectoryInfo[] subDirs = null;

            // First, process all the files directly under this folder
            try
            {
                files = root.GetFiles(string.Format("*.{0}", extension));
            }
            // This is thrown if even one of the files requires permissions greater
            // than the application provides.
            catch (UnauthorizedAccessException e)
            {
                // This code just writes out the message and continues to recurse.
                // You may decide to do something different here. For example, you
                // can try to elevate your privileges and access the file again.
                RhinoApp.WriteLine(e.Message);
            }

            catch (System.IO.DirectoryNotFoundException e)
            {
                RhinoApp.WriteLine(e.Message);
            }

            if (files != null)
            {
                foreach (System.IO.FileInfo fi in files)
                {
                    // In this example, we only access the existing FileInfo object. If we
                    // want to open, delete or modify the file, then
                    // a try-catch block is required here to handle the case
                    // where the file has been deleted since the call to TraverseTree().

                    //Console.WriteLine(fi.FullName);
                    if (extension == "*")
                    {
                        results.Add(fi);
                    }
                    else if (extension.ToUpper() == fi.Extension.ToUpper())
                    {
                        results.Add(fi);
                        Console.WriteLine(fi.FullName);
                    }

                }

                // Now find all the subdirectories under this directory.
                subDirs = root.GetDirectories();

                foreach (System.IO.DirectoryInfo dirInfo in subDirs)
                {
                    // Resursive call for each subdirectory.
                    WalkDirectoryTree(dirInfo, results, extension);
                }
            }
        }

        public static string SubmittalFolder(RhinoDoc doc, int submitNumber, string submitTo)
        {
            string submittalFolder = string.Format("{0}/Documents/Submittals/{1}_{2}_{3}/",
                Find_ProjectFolder(doc), submitNumber, submitTo, DateTime.Today.CTracFormat());

            if (!Directory.Exists(submittalFolder))
            {
                Directory.CreateDirectory(submittalFolder);
            }
            return submittalFolder;
        }
    }
}
