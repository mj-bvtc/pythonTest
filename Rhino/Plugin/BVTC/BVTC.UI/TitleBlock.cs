using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Reflection;

using BVTC.Data.Helpers;
using BVTC.UI.Helpers;

namespace BVTC.UI
{
    public partial class TitleBlock : Form
    {
        public int tabCount { get; set; }
        public TabControl tabCtrl { get; set; }
        public List<Data.Drafting> dataList { get; set; }
        public UI.ComboLists comboLists { get; set; }

        private string icon_folder { get; set; }
        public string iconFolder
        {
            get
            {
                return this.icon_folder;
            }
            set
            {
                this.icon_folder = value;
                this.icons = new Icons(this.icon_folder);
            }
        }
        public Icons icons { get; set; }

        // timer property and start function //
        //public System.Timers.Timer eventTimer { get; set; }
        public System.Windows.Forms.Timer eventTimer { get; set; }

        public void Timer_Setup()
        {
            // setup 2 second timer //
            this.eventTimer = new System.Windows.Forms.Timer();
            this.eventTimer.Enabled = true;
            this.eventTimer.Interval = 2000;    // 2 seconds
            this.eventTimer.Tick += new EventHandler(Timer_Function);
            this.eventTimer.Stop();
        }
        public void Timer_Reset()
        {
            // reset the timer //
            this.eventTimer.Stop();
            this.eventTimer.Start();
        }
        public void Timer_Function(object sender, EventArgs e)
        {
            // stop the timer from continuing to trigger //
            this.eventTimer.Stop();
            this.eventTimer.Enabled = false;
            this.CheckAll_BlockIDs();
            

        }

        public TitleBlock( List<Data.Drafting> dataList, string icon_folder)
        {
            this.iconFolder = icon_folder;
            InitializeComponent();

            this.comboLists = new BVTC.UI.ComboLists();

            this.tabCtrl = AddTabControl();
            this.dataList = dataList;
            for (int i = 0; i < dataList.Count; i++)
            {
                TabPage tab = BuildNewTab(dataList[i]);
            }

            Timer_Setup();
        }

        private TabControl AddTabControl()
        {
            TabControl tabControl = new TabControl();
            tabControl.SuspendLayout();

            tabControl.Name = "TabControl";
            tabControl.SelectedIndex = 0;

            // correctly size tab control //
            tabControl.Size = new Size(275, 910);

            // start the tab count at 0 //
            this.tabCount = 0;

            tabControl.TabIndex = 0;

            this.Controls.Add(tabControl);
            this.ResumeLayout();

            return tabControl;
        }

        private TabPage AddTab(string name)
        {
            /* Add a new tab to the TabControl
                */
            TabPage Tab = new System.Windows.Forms.TabPage();
            Tab.SuspendLayout();

            Tab.Name = "TabPage_" + tabCount.ToString();

            Tab.TabIndex = this.tabCount;
            Tab.Text = name;
            Tab.UseVisualStyleBackColor = true;

            return Tab;
        }

        public TabPage BuildNewTab(Data.Drafting data)
        {
            // Craete new tab and panel //
            TabPage tab = AddTab(data.BlockID);
            PanelUI panel = new PanelUI(this);
            tab.Controls.Add(panel);

            Control c;

            // get tab count as (i) //
            int i = this.tabCount;
            // set width for all controls, for ease of use //
            int width = 150;

            // project number //
            panel.autoLabel(i, "Project Number");
            panel.addReadonly("Readonly_ProjectNumber_" + i.ToString(), data.ProjectNumber, width, true);

            // project name //
            panel.autoLabel(i, "Project Name");
            panel.addReadonly("Readonly_ProjectName_" + i.ToString(), data.ShortDescription, width, true);

            // block ID //
            panel.addSeperator("Seperator", 250, true);
            panel.autoLabel(i, "Block ID");
            if (i == 0)
            {
                panel.autoTextBox(data, i, "BlockID", width - 30, false);
            }
            else
            {
                panel.autoTextBox(data, i, "BlockID", width - 60, false);
                panel.addRemoveButton(i, "RemoveStyle");
            }
            panel.addNewButton(i, "NewStyle");
            // Base Style //
            panel.autoLabel(i, "Base Style");
            panel.addReadonly("TextBox_BaseStyle_" + i.ToString(), data.BaseStyle, width, true);

            // Client ID //
            panel.autoLabel(i, "Client ID");
            panel.autoTextBox(data, i, "ClientID", width - 30, false);
            c = panel.addButton("PullEstimating_Button_" + i.ToString(), "", 25, this.icons.pull, true, panel.PullData_Clicked);
            c.Enabled = false;

            // Estimating ID //
            panel.autoLabel(i, "Estimating ID");
            panel.autoTextBox(data, i, "EstimatingID", width - 30, false);
            c = panel.addButton("PullEstimating_Button_" + i.ToString(), "", 25, this.icons.pull, true, panel.PullData_Clicked);
            c.Enabled = false;

            // Survey ID //
            panel.autoLabel(i, "Survey ID");
            panel.autoTextBox(data, i, "SurveyID", width - 30, false);
            c = panel.addButton("PullSurvey_Button_" + i.ToString(), "", 25, this.icons.pull, true, panel.PullData_Clicked);
            c.Enabled = false;

            // Current User //
            panel.addSeperator("Seperator", 250, true);
            panel.autoLabel(i, "Modeler");
            int index = this.comboLists.DrafterInitials.TryIndexOf(this.dataList[i].User);
            panel.addComboBox("ComboBox_User_" + i.ToString(), this.comboLists.DrafterNames, 
                index, 110, false, panel.QC_Combo_Changed);
            panel.addReadonly("Readonly_User_" + i.ToString(), data.User, 35, true);

            // Checked By //
            panel.autoLabel(i, "Checked By");
            index = this.comboLists.DrafterInitials.TryIndexOf(this.dataList[i].CheckedBy);
            panel.addComboBox("ComboBox_CheckedBy_" + i.ToString(), this.comboLists.DrafterNames, 
                index, 110, false, panel.QC_Combo_Changed);
            panel.addReadonly("Readonly_CheckedBy_" + i.ToString(), this.dataList[i].CheckedBy, 35, true);


            // Approval Date //
            panel.autoLabel(i, "Date");
            panel.addReadonly("Readonly_Date_" + i.ToString(), data.DateCreated.ToShortDateString(), width, true);


            panel.addSeperator("Seperator", 250, true);

            // Sample Name //
            panel.autoLabel(i, "Sample Name");
            panel.autoTextBox(data, i, "Sample", width, true);

            // Drawing Revision //
            panel.autoLabel(i, "Drawing Revision");
            panel.addReadonly("Readyonly_Revision_" + i.ToString(), data.Revision, width, true);

            // Quantity //
            panel.autoLabel(i, "Quantity");
            panel.autoTextBox(data, i, "Quantity", width, true);

            // Glaze //
            panel.autoLabel(i, "Glaze");
            panel.autoTextBox(data, i, "Glaze", width, true);

            // Comments //
            panel.autoLabel(i, "Comments");
            panel.autoTextBox(data, i, "Comments", width, true);

            panel.addSeperator("Seperator", 250, true);

            // Desc Style //
            panel.autoLabel(i, "Description");
            panel.addComboBox("ComboBox_DescStyle_" + i.ToString(), this.comboLists.DescStyle, data.DescStyle, width, true);
            data.DescStyle = this.comboLists.DescStyle.Find_String(data.DescStyle);

            // Desc Shape //
            panel.autoLabel(i, "Style");
            panel.addComboBox("ComboBox_DescShape_" + i.ToString(), this.comboLists.DescShape, data.DescShape, width, true);
            data.DescShape = this.comboLists.DescShape.Find_String(data.DescShape);

            //Desc Orniment //
            panel.autoLabel(i, "Sculpture");
            panel.addComboBox("ComboBox_DescSculpture_" + i.ToString(), this.comboLists.DescSculpture, data.DescSculpture, width, true);
            data.DescSculpture = this.comboLists.DescSculpture.Find_String(data.DescSculpture);

            //Description Orientation //
            panel.autoLabel(i, "Orientation");
            panel.addComboBox("ComboBox_DescOrientation_" + i.ToString(), this.comboLists.DescOrientation, data.DescOrientation, width, true);
            data.DescOrientation = this.comboLists.DescOrientation.Find_String(data.DescOrientation);

            // Description Forming Method //
            panel.autoLabel(i, "Forming Method");
            panel.addComboBox("ComboBox_DescFormingMethod_" + i.ToString(), this.comboLists.DescFormingMethod, data.DescFormingMethod, width, true);
            data.DescFormingMethod = this.comboLists.DescFormingMethod.Find_String(data.DescFormingMethod);

            // Description Region //
            panel.autoLabel(i, "Region");
            panel.addComboBox("ComboBox_DescRegion_" + i.ToString(), this.comboLists.DescRegion, data.DescRegion, width, true);
            data.DescRegion = this.comboLists.DescRegion.Find_String(data.DescRegion);

            // Description Profile //
            panel.autoLabel(i, "Profile");
            panel.autoTextBox(data, i, "Profile", width, true);

            panel.addSeperator("Seperator", 250, true);

            // Block Length //
            panel.autoLabel(i, "Length");
            c = panel.autoTextBox(data, i, "Length", width - 30, false);
            c.Enabled = false;
            panel.addLockButton(i, "Length");

            // Block Height //
            panel.autoLabel(i, "Height");
            c = panel.autoTextBox(data, i, "Height", width - 30, false);
            c.Enabled = false;
            panel.addLockButton(i, "Height");

            // Block Depth //
            panel.autoLabel(i, "Depth");
            c = panel.autoTextBox(data, i, "Depth", width - 30, false);
            c.Enabled = false;
            panel.addLockButton(i, "Depth");

            // Block Volume //
            panel.autoLabel(i, "Volume");
            c = panel.autoTextBox(data, i, "Volume", width - 30, true);
            c.Enabled = false;

            // Block Weight //
            panel.autoLabel(i, "Weight");
            c = panel.autoTextBox(data, i, "Weight", width - 30, true);
            c.Enabled = false;

            /* ~Removed to eliminate circular referances 
            panel.addButton("Button", "Resize Dimensions", width, "", true, panel.Resize_Clicked);

            ~Removed 10-14-16 to save space on UI~
            panel.addSeperator("Seperator", 250, true);
            
            panel.addLabel("Label", "GUID", 50, false);
            panel.addLabel("Label_GUID_" + i.ToString(), data.GUID, 200, true);
            */

            panel.addButton("Button", "Okay", width, null, true, panel.Okay_Button_Clicked);

            panel.layoutPanel();

            // add panel to tab //
            tab.Controls.Add(panel);
            // add tab to tabCtrl //
            this.tabCtrl.Controls.Add(tab);
            // increament up the tabCount //
            this.tabCount += 1;
            return tab;
        }

        public bool CheckAll_BlockIDs()
        {
            
            string baseStyle = null;
            try
            {
                // Get BaseStyle for all blocks //
                List<Data.data> generic = this.dataList.AbstractList();
                baseStyle = generic.Compare_BaseStyle();
            }
            catch (Data.Exceptions.BlockID_Exception blockExcept)
            {
                // blank Block ID was entered //
                Rhino.UI.Dialogs.ShowMessageBox(blockExcept.Message, "Invalid Block Name");
            }
            catch (Data.Exceptions.DataMisMatch_Exception mismatchExcept)
            {
                // show error to users //
                Rhino.UI.Dialogs.ShowMessageBox(mismatchExcept.Message, "Data Mis-Match Exception");

                // ask to to change BaseStyle to //
                DialogResult r = Rhino.UI.Dialogs.ShowEditBox("Rename Block IDs", "Specify a base style to apply to all Block IDs:",
                    this.dataList[0].BlockID.Split('-')[0], false, out baseStyle);

                // change all block ids //
                baseStyle = baseStyle.Split('-')[0];
                
                for (int i = 0; i < this.tabCount; i++)
                {
                    Control[] list = this.Controls.Find("TextBox_BlockID_" + i.ToString(), true);
                    if (list.Length > 0)
                    {
                        if (r == DialogResult.OK)
                        {
                            list[0].Text = string.Format("{0}-{1}", baseStyle, i + 1);
                        }
                        else if (this.dataList[0].BaseStyle != null || this.dataList[0].BaseStyle != "")
                        {
                            list[0].Text = string.Format("{0}-{1}", this.dataList[0].BaseStyle, i + 1);
                        }
                        else
                        {
                            list[0].Text = "";
                        }
                    }
                }
            }
            if (string.IsNullOrEmpty(baseStyle) == true) { return false; }
            else { return true; }
        }
    }


    public class PanelUI : FlowLayoutPanel
    {
        // custom properties for classes //
        public List<Control> controls { get; set; }
        public int tabIndex { get; set; }

        public TitleBlock MainForm { get; set; }

        public bool LengthLock { get; set; }
        public bool HeightLock { get; set; }
        public bool DepthLock { get; set; }

        public PanelUI(TitleBlock mainform)
        {
            this.MainForm = mainform;

            this.tabIndex = 0;
            this.AutoScroll = true;
            this.FlowDirection = FlowDirection.LeftToRight;
            this.WrapContents = true;

            // size the panel //
            this.Size = new Size(300, 875);

            // initialize container for controls //
            this.controls = new List<Control>();
        }

        public static TitleBlock GetMainForm(object sender)
        {
            /* This isn't great code, there is no error checking happening here.
             * But it should work as long as its called from the right place.
             * Not proud of myself -PAS-
             */

            // step back from tab to parent form //
            Control c = (Control)sender;
            PanelUI panel = (PanelUI)c.Parent;
            TabPage tab = (TabPage)panel.Parent;
            TabControl tabCtrl = (TabControl)tab.Parent;
            TitleBlock ui = (TitleBlock)tabCtrl.Parent;

            return ui;
        }
        public static TabControl GetTabControl(object sender)
        {
            /* This isn't great code, there is no error checking happening here.
             * But it should work as long as its called from the right place.
             * Not proud of myself -PAS-
             */

            // step back from tab to parent form //
            Control c = (Control)sender;
            PanelUI panel = (PanelUI)c.Parent;
            TabPage tab = (TabPage)panel.Parent;
            TabControl tabCtrl = (TabControl)tab.Parent;
            return tabCtrl;
        }
        public static TabPage GetTabPage(object sender)
        {
            /* This isn't great code, there is no error checking happening here.
             * But it should work as long as its called from the right place.
             * Not proud of myself -PAS-
             */

            // step back from tab to parent form //
            Control c = (Control)sender;
            PanelUI panel = (PanelUI)c.Parent;
            TabPage tab = (TabPage)panel.Parent;
            return tab;
        }

        public Control addButton(string name, string text, int width, Image image, bool breakFlowAfter, EventHandler clickFunction)
        {
            Button c = new System.Windows.Forms.Button();

            c.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            c.AutoEllipsis = false;
            c.Name = name;
            c.Text = text;


            if (image != null)
            {
                c.Image = image;
                c.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
                c.UseVisualStyleBackColor = true;
            }

            c.Height = 25;

            if (width < 0)
                c.Width = width;
            else
                c.AutoSize = true;


            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;
            c.Click += new System.EventHandler(clickFunction);

            if (text == "OK" || text == "Done" || text == "Update")
                c.DialogResult = DialogResult.OK;
            else if (text == "Cancel")
                c.DialogResult = DialogResult.Cancel;

            this.SetFlowBreak(c, breakFlowAfter);

            this.controls.Add(c);
            return c;
        }
        public Control addButton(string name, string text, int width, string filename, bool breakFlowAfter)
        {
            Image image = System.Drawing.Image.FromFile(filename);
            return addButton(name, text, width, image, breakFlowAfter, Button_Clicked);
        }

        public Control addLockButton(int tab, string name)
        {
            Button c = new System.Windows.Forms.Button();

            c.Name = "Button_" + name + "_" + tab.ToString();

            // setup image and set it to button //
            c.Image = this.MainForm.icons.lockIcon;
            
            c.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            c.UseVisualStyleBackColor = true;

            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;
            c.Click += new System.EventHandler(Lock_Clicked);

            // set size //
            c.Width = 25;
            c.Height = 22;

            // set break flow for panel //
            this.SetFlowBreak(c, true);

            this.controls.Add(c);

            return c;
        }
        public Control addNewButton(int tab, string name)
        {
            Button c = new Button();
            c.Name = "Button_" + name + "_" + tab.ToString();

            // setup image and set it to button //
            c.Image = this.MainForm.icons.newIcon;

            c.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            c.UseVisualStyleBackColor = true;

            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;
            c.Click += new System.EventHandler(AddStyle_Clicked);
            // set size //
            c.Width = 25;
            c.Height = 22;

            // set break flow for panel //
            this.SetFlowBreak(c, true);

            this.controls.Add(c);

            return c;
        }
        public Control addRemoveButton(int tab, string name)
        {
            Button c = new Button();
            c.Name = "Button_" + name + "_" + tab.ToString();

            // set image //
            c.Image = this.MainForm.icons.deleteIcon;

            c.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            c.UseVisualStyleBackColor = true;

            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;
            c.Click += new System.EventHandler(RemoveStyle_Clicked);
            // set size //
            c.Width = 25;
            c.Height = 22;

            // set break flow for panel //
            this.SetFlowBreak(c, false);

            this.controls.Add(c);

            return c;
        }

        public Control addLabel(string name, string text, int width, Color color, bool breakFlowAfter)
        {
            /* Add a label to a panel 
                * Input Parameters:
                *      name - Label.Name
                *      text - Label.Text
                *      color - Label.ForeColor
                *      width - if == 0 AutoSize or Label.Width
                *      breakFlowAfter - Panel.SetFlowBreak
                */

            Control c = new System.Windows.Forms.Label();

            c.Name = name;
            c.Text = text;
            c.ForeColor = color;
            if (width > 0)
                c.Width = width;
            else
                c.AutoSize = true;

            // set tab index order //
            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;

            this.SetFlowBreak(c, breakFlowAfter);

            this.controls.Add(c);
            return c;
        }
        public Control addLabel(string name, string text, int width, bool breakFlowAfter)
        {
            // overloaded class to create a label that is by default black //
            return addLabel(name, text, width, Color.Black, breakFlowAfter);
        }
        public Control autoLabel(int i, string text)
        {
            string name = "Label_" + text.Replace(" ", "") + "_" + i.ToString();
            return addLabel(name, text, 100, false);
        }

        public Control addTextBox(string name, string text, int width, bool breakFlowAfter, EventHandler function)
        {
            Control c = addTextBox(name, text, width, breakFlowAfter);
            c.TextChanged += new System.EventHandler(function);
            return c;
        }
        public Control addTextBox(string name, string text, int width, bool breakFlowAfter)
        {
            Control c = new System.Windows.Forms.TextBox();
            c.Name = name;
            c.Text = text;
            c.Width = width;
            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;
            this.SetFlowBreak(c, breakFlowAfter);

            this.controls.Add(c);

            return c;
        }
        public Control autoTextBox(Data.Drafting data, int i, string propName, int width, bool breakFlowAfter)
        {
            string name = "TextBox_" + propName + "_" + i.ToString();
            PropertyInfo property = data.GetType().GetProperty(propName);

            // get text for textBox from data property  and convert to string //
            string text = "";
            if (property.PropertyType != typeof(string))
                text = property.GetValue(data, null).ToString();
            else
                text = (string)property.GetValue(data, null);

            Control c = addTextBox(name, text, width, breakFlowAfter, TextBox_Changed);
            return c;
        }

        public Control addReadonly(string name, string text, int width, bool breakFlowAfter)
        {
            Control c = addTextBox(name, text, width, breakFlowAfter, TextBox_Changed);
            c.Enabled = false;
            return c;
        }

        public Control addComboBox(string name, List<string> items, int initialIndex, int width, bool breakFlowAfter, EventHandler function)
        {
            /*
            Adds a multiple selection drop - down list control to the panel.
                Note: This control currently takes up too much vertical space on the form.
                There seems to be a layout bug in the Winforms auto - size code.
                Parameters:
                name: The name for the control. You may pass "" if you don't need to
                    reference the control by name.
                items: A list of strings, one for each choice from the box.
                initialIndex: The zero based index of which item is initially selected.
                breakFlowAfter: Pass True to have the next control on a new line.
                    False to have the next control on the same line if there is room.
                delegate: The event handler when the SelectedIndexChanged event is raised. 
                    Pass None if you don't need to handle the event. 
            Returns:
                The control which was added.
            */
            ComboBox c = new ComboBox();
            c.Name = name;
            c.Width = width;

            foreach (string item in items)
            { c.Items.Add(item); }

            c.DropDownStyle = ComboBoxStyle.DropDownList;
            c.SelectedIndex = initialIndex;
            c.TabIndex = this.tabIndex;
            this.tabIndex += 1;

            c.SelectedIndexChanged += function;
            this.SetFlowBreak(c, breakFlowAfter);
            this.controls.Add(c);
            return c;
        }
        public Control addComboBox(string name, List<string> items, string initialString, int width, bool breakFlowAfter, EventHandler function)
        {
            /* Overlaoded class to automatically make a choice about the which string to preselect for comboBox.
                */
            int index = 0;
            if (items.Contains(initialString) == true)
                index = items.IndexOf(initialString);

            return addComboBox(name, items, index, width, breakFlowAfter, function);
        }
        public Control addComboBox(string name, List<string> items, string initialString, int width, bool breakFlowAfter)
        {
            /* Overlaoded class to automatically make a choice about the which string to preselect for comboBox.
                */
            int index = 0;
            if (items.Contains(initialString) == true)
                index = items.IndexOf(initialString);

            return addComboBox(name, items, index, width, breakFlowAfter, ComboBox_Changed);
        }

        public Control addSeperator(string name, int width, bool breakFlowAfter)
        {
            /*
            Adds a separator(horizontal bar) to the panel.This is normally
                simply an organization aide. 
            Parameters:
            name: The name for the control. You may pass "" if you don't need to
                    reference the control by name.
                width: The horizontal size in pixels for the control.
                breakFlowAfter: Pass True to have the next control on a new line.
                    False to have the next control on the same line if there is room.
            Returns:
                The control which was added.
            */
            Control c = new GroupBox();
            c.Size = new System.Drawing.Size(width, 8); // 8 makes it a horizontal bar
            c.Margin = new System.Windows.Forms.Padding(3, 6, 3, 10); // 5 is to align with other controls vertically
            c.TabStop = false;
            this.SetFlowBreak(c, breakFlowAfter);
            this.controls.Add(c);
            return c;
        }

        public void TextBox_Changed(object sender, EventArgs args)
        {
            // cast into TextBox //
            TextBox textBox = (TextBox)sender;

            // get propName of textBox //
            if (textBox.Name.Contains('_') == false) { return; }
            string propName = textBox.Name.Split('_')[1];

            // try to parse current tab //
            int i;
            System.Int32.TryParse(textBox.Name.Split('_')[2], out i);

            // get main form //
            TitleBlock ui = GetMainForm(sender);
            // get data ui //
            Data.Drafting data = ui.dataList[i];

            // return if nothing is in text box //
            if (string.IsNullOrEmpty(textBox.Text) == true)
            {
                // clear data from property if data is deleted //
                if (data.HasProperty(propName) == true)
                {
                    //Rhino.RhinoApp.WriteLine(string.Format("Cleared data.{0}", propName));
                    data.GetType().GetProperty(propName).SetValue(data, null, null);
                }
                return;
            }

            
            // try to update the data //
            try
            {
                data.SetAttr_FromTextBox(propName, textBox.Text);

                // special handling for Block IDs //
                if (propName == "BlockID")
                {
                    // change tab name is check passes //
                    if (textBox.Text.CheckBlockID(false))
                    {
                        TabPage tab = GetTabPage(sender);
                        tab.Text = textBox.Text;
                    }
                    ui.Timer_Reset();
                }
                
            }
            catch (Exception)
            {
                this.SuspendLayout();
                object value = data.GetType().GetProperty(propName).GetValue(data, null);
                textBox.Text = value.ToString();
                this.ResumeLayout(false);
            }
        }

        public void Button_Clicked(object sender, EventArgs e)
        {

        }
        public void Okay_Button_Clicked(object sender, EventArgs e)
        {
            // get main form handle //
            TitleBlock ui = GetMainForm(sender);

            // bool check results //
            bool check = true;

            // stop timer from double counting //
            ui.eventTimer.Stop();
            ui.eventTimer.Enabled = false;
            if (ui.CheckAll_BlockIDs() == false) { check = false; }


            // close dialog and return if check == true //
            if (check == true)
            {
                ui.DialogResult = DialogResult.OK;
            }
            else
            {
                Rhino.RhinoApp.WriteLine("Checks did not pass.");
            }
            
        }

        public void ComboBox_Changed(object sender, EventArgs e)
        {
            ComboBox combo = (ComboBox)sender;
            TitleBlock ui = GetMainForm(combo);

            // try to parse current tab //
            int i; Int32.TryParse(combo.Name.Split('_')[2], out i);

            // get propName of textBox //
            if (combo.Name.Contains('_') == false) { return; }
            string propName = combo.Name.Split('_')[1];

            // get selected index //
            int selected = combo.SelectedIndex;
            PropertyInfo property = ui.comboLists.GetType().GetProperty(propName);
            if (property == null) { return; }
            List<string> items = (List<string>)property.GetValue(ui.comboLists, null);
            string value = items[selected];

            // set value in data class //
            Data.Drafting data = ui.dataList[i];
            if (data.HasProperty(propName) == true)
            {
                if (value == "None")
                {
                    data.GetType().GetProperty(propName).SetValue(data, null, null);
                }
                else
                {
                    data.GetType().GetProperty(propName).SetValue(data, value, null);
                }
            }
        }

        public void QC_Combo_Changed(object sender, EventArgs e)
        {
            ComboBox combo = (ComboBox)sender;
            TitleBlock ui = GetMainForm(combo);

            // get propName of textBox //
            if (combo.Name.Contains('_') == false) { return; }
            string propName = combo.Name.Split('_')[1];

            // try to parse current tab //
            int i; int.TryParse(combo.Name.Split('_')[2], out i);

            // get selected index //
            int selected = combo.SelectedIndex;

            // get QC initials //
            string initials = ui.comboLists.DrafterInitials[selected];

            for (int n = 0; n < ui.tabCount; n++)
            {
                Control[] controls = ui.Controls.Find(
                    string.Format("Readonly_{0}_{1}", propName, n), true);
                if (controls.Length > 0)
                {
                    Control c = controls[0];
                    c.Text = initials;
                }

                // set other controls to match //
                if (n != i)
                {
                    ui.SuspendLayout();
                    controls = ui.Controls.Find(string.Format("ComboBox_{0}_{1}", propName, n), true);
                    if (controls.Length > 0)
                    {
                        ComboBox comboBox = (ComboBox)controls[0];
                        comboBox.SelectedIndex = selected;
                    }
                    ui.ResumeLayout(false);
                }
            }
        }

        public void Lock_Clicked(object sender, EventArgs e)
        {
            Button button = (Button)sender;
            string tab = button.Name.Split('_')[2];
            string type = button.Name.Split('_')[1];
            string controlName = "TextBox_" + type + "_" + tab;

            // find control to lock or unlock //
            Panel panel = (Panel)button.Parent;
            Control c = panel.Controls.Find(controlName, true)[0];

            // set readony property //
            if (c.Enabled == true)
            {
                c.Enabled = false;
                button.Image = this.MainForm.icons.lockIcon;
            }
            else
            {
                c.Enabled = true;
                button.Image = this.MainForm.icons.unlockIcon;
            }
        }

        public void AddStyle_Clicked(object sender, EventArgs e)
        {
            // get main form and sending control //
            TitleBlock ui = GetMainForm(sender);
            Button button = (Button)sender;

            // try to parse current tab //
            int i; int.TryParse(button.Name.Split('_')[2], out i);

            // if there is only one style //
            if (i == 0 && ui.tabCount == 1)
            {
                Data.Drafting d = ui.dataList[i];
                Control c = ui.Controls.Find("TextBox_BlockID_0", true)[0];
                c.Text = d.BaseStyle + "-" + ui.tabCount.ToString();
            }

            // duplicate data from current tab //
            Data.Drafting data = (Data.Drafting)ui.dataList[i].Duplicate();
            
            // clear init Block ID so it won't overwrite //
            data.InitBlockID = null;
            data.Updated = true;
            data.BlockID = data.BaseStyle + "-" + (ui.tabCount + 1).ToString();

            // add new duplicate data to ui.dataList //
            ui.dataList.Add(data);

            // add new tab to ui //
            TabPage tab = ui.BuildNewTab(data);

            ui.tabCtrl.SelectedTab = tab;
        }

        public void RemoveStyle_Clicked(object sender, EventArgs e)
        {
            // get main form and sending control //
            TitleBlock ui = GetMainForm(sender);
            TabControl tabCtrl = GetTabControl(sender);
            Button button = (Button)sender;

            // try to parse current tab //
            int i; int.TryParse(button.Name.Split('_')[2], out i);

            // set data.deleted = true //
            ui.dataList[i].deleted = true;
            ui.dataList[i].Quantity = 0;

            TabPage tab = GetTabPage(sender);
            tabCtrl.Controls.Remove(tab);

        }

        public void PullData_Clicked(object sender, EventArgs e)
        {
            Rhino.RhinoApp.WriteLine("PullData Clicked");
        }

        public void layoutPanel()
        {
            // add all controls that were accumulated to panel //
            this.SuspendLayout();
            foreach (Control c in this.controls)
            {
                this.Controls.Add(c);
            }
            this.ResumeLayout();
        }
    }

}
