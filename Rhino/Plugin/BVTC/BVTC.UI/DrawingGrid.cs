using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data;
using System.Windows.Forms;

using BVTC.UI.Helpers;
using Rhino;



namespace BVTC.UI
{
    

    public class DrawingGrid : DisplayDT
    {
        public Collections.SubmittalType submittalType { get; set; }
        public Collections.SubmittalTarget submitTo { get; set; }
        public int submittalNumber { get; set; }

        public DrawingGrid(DataTable dt, string title = "", bool addRows = true) 
            : base(dt, title, addRows)
        {
            setup();
        }
        public DrawingGrid(DataTable dt, List<string> readOnlyColumns, string title = "", bool addRows = true) 
            : base(dt, readOnlyColumns, title, addRows)
        {
            setup();
        }

        private void setup()
        {
            this.dataGridView1.AddComboBoxColumn(0, "Print", "Print");

            this.dataGridView1.ColumnVisible("GUID", false);
            this.dataGridView1.ColumnVisible("ClientPDF", false);
            this.dataGridView1.ColumnVisible("ShopPDF", false);
            this.dataGridView1.ColumnVisible("Project Number", false);
            this.dataGridView1.ColumnVisible("Path", false);

            this.dataGridView1.AllowUserToAddRows = false;

            this.dataGridView1.ResizeGridView();

            // add new event for checking all check boxes //
            dataGridView1.ColumnHeaderMouseDoubleClick += new DataGridViewCellMouseEventHandler(dataGridView1_ColumnHeaderMouseDoubleClick);

            // add combo box for submittal choices //
            ComboBox c = new ComboBox();
            c.Name = "Submittal_ComboBox";
            string[] options = Enum.GetNames(typeof(Collections.SubmittalType));
            c.Items.AddRange(options);
            c.DropDownStyle = ComboBoxStyle.DropDownList;
            c.SelectedIndexChanged += SubmittalCombo_Changed;
            c.SelectedIndex = 0;

            this.panel.SetFlowBreak(c, true);
            this.panel.Controls.Add(c);

            // add combo box for submittal choices //
            ComboBox tar = new ComboBox();
            tar.Name = "Submittal_ComboBox";
            string[] locations = Enum.GetNames(typeof(Collections.SubmittalTarget));
            tar.Items.AddRange(locations);
            tar.DropDownStyle = ComboBoxStyle.DropDownList;
            tar.SelectedIndexChanged += TargetCombo_Changed;
            tar.SelectedIndex = 0;

            this.panel.SetFlowBreak(tar, true);
            this.panel.Controls.Add(tar);
        }

        private void dataGridView1_ColumnHeaderMouseDoubleClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            int index = e.ColumnIndex;

            if (dataGridView1.Columns[e.ColumnIndex].GetType() == typeof(DataGridViewCheckBoxColumn))
            {
                foreach (DataGridViewRow row in dataGridView1.Rows)
                {
                    DataGridViewCheckBoxCell chk = (DataGridViewCheckBoxCell)row.Cells[e.ColumnIndex];
                    chk.Value = true;
                }
                
            }
        }

        private void SubmittalCombo_Changed(object source, EventArgs e)
        {
            // cast object into ComboBox //
            ComboBox cb = (ComboBox)source;
            // set submittal type //
            this.submittalType = (Collections.SubmittalType)cb.SelectedIndex;
        }
        private void TargetCombo_Changed(object source, EventArgs e)
        {
            // cast object into ComboBox //
            ComboBox cb = (ComboBox)source;
            // set submittal type //
            this.submitTo = (Collections.SubmittalTarget)cb.SelectedIndex;
        }
    }
}
