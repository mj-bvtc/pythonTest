using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace BVTC.osTools
{
    public class FileShuffler
    {
        public string finalDestination { get; set; }
        public string fileExtension { get; set; }

        // create read only property //
        private bool moved { get; set; }
        public bool Moved
        {
            get { return this.moved; }
        }
        // get the min size of a file //
        public long MinSize { get; set; }

        public FileShuffler(string toPath)
        {
            // setup stuff here //
            this.finalDestination = toPath;
            this.moved = false;
            this.fileExtension = ".PDF";
            this.MinSize = 2500;

        }

        public void OnFileSystemWatcherCreated(object source, System.IO.FileSystemEventArgs args)
        {

            // check if the created file is in fact a PDF //
            System.IO.FileInfo info = new System.IO.FileInfo(args.FullPath);
            if (info.Extension.ToUpper() == ".PDF")
            {
                /*
                // Check for empty files not currently working //
                if (FileSize(args.FullPath) < this.MinSize)
                {
                    throw new Exceptions.BlankPDF_Exception(string.Format(
                        "file {0} is blank", args.FullPath));
                }
                */
                this.moved = MoveFile(args.FullPath, this.finalDestination);

                // stop this watcher from continuing to raise events //
                System.IO.FileSystemWatcher watcher = (System.IO.FileSystemWatcher)source;
                watcher.EnableRaisingEvents = false;
            }
            

        }

        public static bool MoveFile(string fromPath, string toPath, double timer = 5)
        {
            DateTime end = DateTime.Now.AddSeconds(timer);

            // remove the old PDF if it exists //
            if (System.IO.File.Exists(toPath))
            {
                if (FileTools.IsFileLocked(toPath))
                {
                    throw new System.IO.IOException(
                        string.Format("file {0} is locked", toPath));
                }
                System.IO.File.Delete(toPath);
            }

            // make sure the destination directory exist //
            if (new System.IO.FileInfo(toPath).Directory.Exists == false)
            {
                throw new FieldAccessException(string.Format(
                    "Directory '{0}' does not exist.", 
                    new System.IO.FileInfo(toPath).Directory.FullName));
            }

            bool moved = false;
            // while loop attempts to move file //
            while (moved == false)
            {
                try
                {
                    System.IO.File.Move(fromPath, toPath);
                    moved = true;
                    return moved;
                }
                // catch access errors on target file //
                catch (System.IO.IOException)
                {
                    // check how long we have been waiting //
                    if (DateTime.Now > end)
                    {
                        // throw error if wait is too long //
                        throw new FieldAccessException(
                            string.Format("File '{0}' could not be accessed.", fromPath));
                    }
                }
            }
            return moved;
        }

        public static bool DeleteFile(string path, double timer = 3)
        {
            bool deleted = false;
            DateTime end = DateTime.Now.AddSeconds(timer);
            while(deleted == false)
            {
                try
                {
                    System.IO.File.Delete(path);
                    deleted = true;
                }
                catch
                {
                    // do something to wait //
                    Thread.SpinWait(1);
                }

                if (DateTime.Now > end)
                {
                    break;
                }
            }


            return deleted;

        }

        public static long FileSize(string path, bool waitForAccess = true, double timer = 10)
        {
            DateTime end = DateTime.Now.AddSeconds(timer);

            if (waitForAccess == true)
            while (FileTools.IsFileLocked(path) == false)
                {
                    Thread.SpinWait(1);
                    if (DateTime.Now > end) { break; }
                }
            return new System.IO.FileInfo(path).Length;
        }
    }
}
