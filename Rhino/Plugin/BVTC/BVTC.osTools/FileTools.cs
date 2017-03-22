using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace BVTC.osTools
{
    public class FileTools
    {
        public static bool IsFileLocked(FileInfo file, FileAccess accessMode = FileAccess.ReadWrite)
        {
            FileStream stream = null;

            try
            {
                stream = file.Open(FileMode.Open, accessMode, FileShare.None);
            }
            catch (IOException)
            {
                //the file is unavailable because it is:
                //still being written to
                //or being processed by another thread
                //or does not exist (has already been processed)
                return true;
            }
            finally
            {
                if (stream != null)
                    stream.Close();
            }

            //file is not locked
            return false;
        }
        public static bool IsFileLocked(string filePath, FileAccess accessMode = FileAccess.ReadWrite)
        {
            return IsFileLocked(new FileInfo(filePath), accessMode);
        }

        public static bool IsFileUpToDate(string samplePath, string checkPath)
        {
            bool updated = false;

            // make sure the sample file exists //
            if (!File.Exists(samplePath))
            {
                throw new FileNotFoundException(
                    string.Format("file {0} does not exist", samplePath));
            }

            // return false if checkpath is empty //
            if (string.IsNullOrEmpty(checkPath) || !File.Exists(checkPath)) { return updated; }

            // get file info to compare //
            FileInfo sampleInfo = new FileInfo(samplePath);
            FileInfo checkInfo = new FileInfo(checkPath);
            if (sampleInfo.LastWriteTime <= checkInfo.LastWriteTime)
            {
                return true;
            }

            return updated;
        }

        public static string  WalkDirectoryTree(System.IO.DirectoryInfo root,
            List<System.IO.FileInfo> results, string extension = "*")
        {
            string errors = "";
            System.IO.FileInfo[] files = null;
            System.IO.DirectoryInfo[] subDirs = null;

            // First, process all the files directly under this folder
            try
            {
                files = root.GetFiles(string.Format("*.*"));
            }
            // This is thrown if even one of the files requires permissions greater
            // than the application provides.
            catch (UnauthorizedAccessException e)
            {
                // This code just writes out the message and continues to recurse.
                // You may decide to do something different here. For example, you
                // can try to elevate your privileges and access the file again.
                errors += e.Message + Environment.NewLine;
            }

            catch (System.IO.DirectoryNotFoundException e)
            {
                errors += e.Message + Environment.NewLine;
            }

            if (files != null)
            {
                foreach (System.IO.FileInfo fi in files)
                {
                    // In this example, we only access the existing FileInfo object. If we
                    // want to open, delete or modify the file, then
                    // a try-catch block is required here to handle the case
                    // where the file has been deleted since the call to TraverseTree().

                    if (extension == "*")
                    {
                        results.Add(fi);
                    }
                    else if (extension.ToUpper() == fi.Extension.ToUpper())
                    {
                        results.Add(fi);
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
            return errors;
        }
    }
}
