using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Windows.Forms;
using BVTC.Data.Helpers;

namespace BVTC.UI.Helpers
{
    public static class Object_Extensions
    {
        // I'm pretty sure this isn't need anymore //
        // PAS 12-2-16 //
        public static bool Verify_Input(this object sender)
        {
            bool verified = true;

            // get propName of Control //
            Control c = (Control)sender;
            if (c.Name.Split('_').Length != 3)
            {
                verified = false;
            }
            string propName = c.Name.Split('_')[1];

            // get the current tab number //
            int i; System.Int32.TryParse(c.Name.Split('_')[2], out i);

            string value = "";
            // sub-routine to deal with text box input //
            if (sender.GetType() == typeof(TextBox))
            {
                TextBox textBox = (TextBox)sender;
                value = textBox.Text;
            }

            // sub-routine to deal with combo boxes //
            if (sender.GetType() == typeof(ComboBox))
            {
                ComboBox combo = (ComboBox)sender;
                value = combo.SelectedItem.ToString();
            }


            // deal with specific criteria per field //
            if (propName == "BlockID")
                if (value.CheckBlockID(false) == false)
                {
                    verified = false;
                }
                else
                {
                    // rename tab to be correct block id //
                    TabPage tab = PanelUI.GetTabPage(sender);
                    tab.Text = value;

                    // set new base style //
                    Control[] list = tab.Controls.Find("TextBox_" + "BaseStyle" + "_" + i.ToString(), true);
                    if (list.Length > 0)
                        list[0].Text = value.GetBaseStyle();

                    // set timer //
                    TitleBlock ui = PanelUI.GetMainForm(sender);
                    ui.Timer_Reset();



                }

            if (value == "")
            {
                verified = false;
            }


            return verified;
        }

    }
}
