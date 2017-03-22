using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using BVTC.UI.Helpers;
using BVTC.RhinoTools.Helpers;



namespace BVTC.UI
{
    public partial class DisplayDT : Form
    {
        public DataGridView dataGrid
        {
            get { return this.dataGridView1; }
        }
        public FlowLayoutPanel panel
        {
            get { return this.flowLayoutPanel1; }
        }

        public DisplayDT(DataTable dt, string title = "", bool addRows = true)
        {
            // create page layout //
            InitializeComponent();

            // change setting for dataGridView //
            dt.TrimHeadings();
            dt.TrimWhiteSpace();

            this.dataGridView1.DataSource = dt;
            
            // change settings for user input //
            this.dataGridView1.AllowUserToAddRows = addRows;

            // change title according to input //
            if (string.IsNullOrEmpty(title) == false) { this.Text = title; }

            // last resize gridView //
            this.dataGridView1.ResizeGridView();

        }

        public DisplayDT(DataTable dt, List<string> readOnlyColumns, string title = "", 
            bool addRows = true)
        {
            // create page layout //
            InitializeComponent();

            // change setting for dataGridView //
            dt.TrimHeadings();
            dt.TrimWhiteSpace();

            this.dataGridView1.DataSource = dt;
            this.dataGridView1.ResizeGridView();
            this.dataGridView1.ReadOnlyColumns(readOnlyColumns);

            // change settings for user input //
            this.dataGridView1.AllowUserToAddRows = addRows;

            // change title according to input //
            if (string.IsNullOrEmpty(title) == false) { this.Text = title; }

            
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
