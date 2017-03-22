using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Rhino;

namespace BVTC.UI
{
    

    public partial class Stock : Form
    {
        //new instance of CTrac
        Repositories.CTrac CTrac = new Repositories.CTrac();

        //setting up stock dataclass
        public Data.Stock.StockData dd = new Data.Stock.StockData();


        public Stock(Data.Stock.StockData stockdata)
        {
            InitializeComponent();

            //sets intial/default form data
            dd = stockdata;
            textbox_pNum.Text = dd.ProjectNumber;
            textbox_pName.Text = dd.ProjectName;
            comboBox_method.SelectedItem = "CNC";
            comboBox_sculpture.SelectedItem = "No";


            //communicate with CTrac to update mold : needs to populate only once
            updateMold();
            comboBox_mold.SelectedIndex = 0; //default setting = first in list

            //update quantity  : refresh as mold selection changes
            updateQty();


            //update drawings : refresh as mold selection changes
            updateDwgs();



            
        }

        private void button_accept_Click(object sender, EventArgs e)
        {
            //when changes accepted, close form and set data
            RhinoApp.WriteLine("Sending data!");
            this.Visible = false;

            useExtension();

            //set remaining data
            string cleanPart = Repositories.StringExtentions.correctStringOneAnd(label_currentMold.Text); //reformat part to not have two &&
            dd.Part = cleanPart;
            dd.Drawings = string.Join(",", listBox_drawings.Items.Cast<string>());
            dd.IsCncSculpture = checkBox_cncSculpt.Checked;
            if (comboBox_sculpture.Text == "Yes") { dd.IsSculpture = true; } else { dd.IsSculpture = false; };
            dd.Method = comboBox_method.Text;
            dd.Quantity = Int32.Parse(textbox_qty.Text);
            dd.Shrinkage = float.Parse(textBox_shrink.Text);
            dd.UseMold = comboBox_mold.Text;

            //dialogresult ok allows for verification that data is acceptable in main stockdrawing command
            this.DialogResult = DialogResult.OK;

        }

        private void comboBox_mold_SelectedIndexChanged(object sender, EventArgs e)
        {
            useExtension();
            updateDwgs();
            updateQty();
            button_accept.Enabled = true;
        }

        private void textbox_part_TextChanged(object sender, EventArgs e)
        {
            label_currentMold.Text = Repositories.StringExtentions.correctStringTwoAnds(comboBox_mold.Text) + "_" + textbox_part.Text;
            useExtension();
        }

        private void comboBox_sculpture_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox_sculpture.Text == "Yes")
            {
                checkBox_cncSculpt.Enabled = true;
                checkBox_cncSculpt.Visible = true;
            }
            else
            {
                checkBox_cncSculpt.Enabled = false;
                checkBox_cncSculpt.Checked = false;
                checkBox_cncSculpt.Visible = false;
            }

        }

        public void useExtension()
        {
            if (
                textbox_part.Text == "0" || 
                textbox_part.Text == "1" ||
                textbox_part.Text == "" || 
                string.IsNullOrWhiteSpace(textbox_part.Text) || 
                string.IsNullOrEmpty(textbox_part.Text))
            {
                label_currentMold.Text = Repositories.StringExtentions.correctStringTwoAnds(comboBox_mold.Text);
            }
            else
            {
                label_currentMold.Text = Repositories.StringExtentions.correctStringTwoAnds(comboBox_mold.Text) + "_" + textbox_part.Text;
            }

            return;
        }

        public void updateQty()
        {
            //update quantity  : updates as mold selection changes
            string cmd2 = "CALL Sum_UseMold('";
            cmd2 += string.Join("','", dd.ProjectNumber, comboBox_mold.Text);
            cmd2 += "')";
            DataTable qtyDt = CTrac.CommandToDataTable(cmd2);
            textbox_qty.Text = qtyDt.Rows[0][0].ToString();
        }

        public void updateDwgs()
        {

            string cmd3 = "CALL Drawings_By_Mold('";
            cmd3 += string.Join("','", dd.ProjectNumber, comboBox_mold.Text);
            cmd3 += "')";
            List<string> drawings = CTrac.CommandToList(cmd3);
            listBox_drawings.Items.Clear(); //refreshes list to prevent duplicates
            foreach (var dwg in drawings)
            {
                listBox_drawings.Items.Add(dwg);
            }
        }

        public void updateMold()
        {
            //populate mold combobox
            string cmd = "CALL Distinct_UseMold('";
            cmd += dd.ProjectNumber;
            cmd += "')";
            List<string> moldList = CTrac.CommandToList(cmd);
            foreach (string mold in moldList)
            {
                comboBox_mold.Items.Add(mold);
                //RhinoApp.WriteLine(mold);
            }

            //display concatenated part = mold + part number
            label_currentMold.Text = Repositories.StringExtentions.correctStringTwoAnds(comboBox_mold.Text) + "_" + textbox_part.Text;
        }

    }
}
