using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;

namespace BVTC.UI
{
    public partial class ProjectBrowser : Form
    {
        ///new datatable, and variables///
        public DataTable dt = new DataTable(); //new datatable instance
        public Data.Stock.StockData dd = new Data.Stock.StockData();
        

        ///main method, project name and number///
        public ProjectBrowser(Data.Stock.StockData sd)
        {
            InitializeComponent();
            Repositories.Pervasive CTrac = new Repositories.Pervasive("10.100.100.6", "CTrac1");
            CTrac.OpenDB();
            string cmd = "Call Get_ProjectsAndNumbers";
            dt = CTrac.CommandToDataTable(cmd);
            CTrac.CloseDB();
            
        }

        
        private void button_accept_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.OK;
            this.Close();
            
        }

        private void textBox_pNameInput_TextChanged(object sender, EventArgs e)
        {
            listBox_pNameResults.Items.Clear();
            string pat = textBox_pNameInput.Text;
            foreach (DataRow row in dt.Rows)
            {
                if (Regex.IsMatch(row["\"Short Description\""].ToString(), pat, RegexOptions.IgnoreCase))
                {
                    listBox_pNameResults.Items.Add(row["\"Short Description\""].ToString());
                }
            }
        }
        private void listBox_pNameResults_SelectedValueChanged(object sender, EventArgs e)
        {
            try
            {

                dd.ProjectName = listBox_pNameResults.SelectedItem.ToString(); //set var pName to selected item
                button_accept.Enabled = true; //enable button
                foreach (DataRow row in dt.Rows)
                {
                    if (row["\"Short Description\""].ToString() == dd.ProjectName)
                    {
                        dd.ProjectNumber = row["\"Project Number\""].ToString();
                    }
                }
                label_pnum.Text = dd.ProjectNumber; // display pName label on UI
                label_pName.Text = dd.ProjectName;
                label_pName.Visible = true; //show label
                label_pnum.Visible = true;
            }
            catch
            { }
        }

        private void ProjectBrowser_Load(object sender, EventArgs e)
        {

        }
    }
}
