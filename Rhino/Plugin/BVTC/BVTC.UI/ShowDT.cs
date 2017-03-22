using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows;

using BVTC.UI.Helpers;
using BVTC.RhinoTools.Helpers;

namespace BVTC.UI
{
    public partial class ShowDT : Form
    {
        public ShowDT(DataTable dt)
        {

            InitializeComponent();
            dt.TrimWhiteSpace();
            this.dataGridView1.DataSource = dt;
            this.dataGridView1.ResizeGridView();
        }

        private void Auto_Resize(object sender, DataGridViewCellEventArgs e)
        {
            if (sender.GetType() == typeof(DataGridView))
            {
                DataGridView grid = (DataGridView)sender;
                grid.ResizeGridView();
            }
            
        }
    }
}
