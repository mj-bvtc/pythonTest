using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

using Rhino;
using BVTC.Data.Helpers;

namespace BVTC.UI
{
    public partial class ProjectInfo : Form
    {
        public string ProjectNumber { get; set; }
        public string ProjectName { get; set; }

        public ProjectInfo(RhinoDoc doc)
        {
            InitializeComponent();

            string projName = BVTC.RhinoTools.FileStructure.Find_ProjectFolder(doc);

            // pull list of project short descriptions from C-Trac //
            List<string> list = new Repositories.CTrac().Get_Projects();
            foreach (string item in list)
            {
                this.comboBox_ShortDescription.Items.Add(item);
            }

        }

        public ProjectInfo(RhinoDoc doc, string selection)
        {
            InitializeComponent();

            string projName = BVTC.RhinoTools.FileStructure.Find_ProjectFolder(doc);

            List<string> list = new Repositories.CTrac().Get_Projects();

            foreach (string item in list)
            {
                this.comboBox_ShortDescription.Items.Add(item);
            }

            int index = 0;
            if (list.Contains(selection) == false)
            {
                selection = list.LevenshteinFind(selection);
            }


            index = list.IndexOf(selection);
            this.comboBox_ShortDescription.SelectedIndex = index;
        }

        private void comboBox_ShortDescription_SelectedIndexChanged(object sender, EventArgs e)
        {
            ComboBox combo = (ComboBox)sender;
            int i = combo.SelectedIndex;
            string selected = (string)combo.Items[i];

            // don't make query for blank entry //
            string pNum = "";
            if (string.IsNullOrEmpty(selected) == false)
            {
                pNum = new Repositories.CTrac().Get_ProjectNumber(selected);
            }
            
            // if data found add it to class property //
            if(pNum != "")
            {
                this.ProjectName = selected;
                this.ProjectNumber = pNum;

                this.textBox_ProjectNumber.Text = pNum;
            }

        }
    }
}
