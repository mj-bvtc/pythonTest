using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Drawing;

using BVTC.RhinoTools.Helpers;

namespace BVTC.UI
{
    public class Icons
    {
        private string imageFolder { get; set; }
        public Icons(string _imageFolder)
        {
            this.imageFolder = _imageFolder;
        }

        // lock icon //
        private Image lock_icon { get; set; }
        public Image lockIcon
        {
            get
            {
                // check if data is present //
                if (this.lock_icon != null)
                {
                    return this.lock_icon;
                }

                // get and set new image //
                string path = this.imageFolder + "lock.png";
                if (System.IO.File.Exists(path) == true)
                {
                    this.lock_icon = Image.FromFile(path);
                    return this.lock_icon;
                }
                throw new Exception("Unable to locate image: " + path);
            }
        }

        // unlock icon //
        private Image unlock_icon { get; set; }
        public Image unlockIcon
        {
            get
            {
                // check if data is present //
                if (this.unlock_icon != null)
                {
                    return this.unlock_icon;
                }

                // get and set new image //
                string path = this.imageFolder + "unlock.png";
                if (System.IO.File.Exists(path) == true)
                {
                    this.unlock_icon = Image.FromFile(path);
                    return this.unlock_icon;
                }
                throw new Exception("Unable to locate image: " + path);
            }
        }

        // new icon //
        private Image new_icon { get; set; }
        public Image newIcon
        {
            get
            {
                // check if data is present //
                if (this.new_icon != null)
                {
                    return this.new_icon;
                }

                // get and set new image //
                string path = this.imageFolder + "new.png";
                if (System.IO.File.Exists(path) == true)
                {
                    this.new_icon = Image.FromFile(path);
                    return this.new_icon;
                }
                throw new Exception("Unable to locate image: " + path);
            }
        }
        
        // delete icon //
        private Image delete_Icon { get; set; }
        public Image deleteIcon
        {
            get
            {
                // check if data is present //
                if (this.delete_Icon != null)
                {
                    return this.delete_Icon;
                }

                // get and set new image //
                string path = this.imageFolder + "delete.png";
                if (System.IO.File.Exists(path) == true)
                {
                    this.delete_Icon = Image.FromFile(path);
                    return this.delete_Icon;
                }
                throw new Exception("Unable to locate image: " + path);
            }
        }

        // pull icon //
        private Image pull_icon { get; set; }
        public Image pull
        {
            get
            {
                // check if data is present //
                if (this.pull_icon != null)
                {
                    return this.pull_icon;
                }

                // get and set new image //
                string path = this.imageFolder + "pull.png";
                if (System.IO.File.Exists(path) == true)
                {
                    this.pull_icon = Image.FromFile(path);
                    return this.pull_icon;
                }
                throw new Exception("Unable to locate image: " + path);
            }
        }

    }
}
