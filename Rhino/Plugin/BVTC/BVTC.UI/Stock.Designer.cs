namespace BVTC.UI
{
    partial class Stock
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label_currentMold = new System.Windows.Forms.Label();
            this.textBox_shrink = new System.Windows.Forms.TextBox();
            this.button_accept = new System.Windows.Forms.Button();
            this.textbox_pNum = new System.Windows.Forms.TextBox();
            this.listBox_drawings = new System.Windows.Forms.ListBox();
            this.label1 = new System.Windows.Forms.Label();
            this.checkBox_cncSculpt = new System.Windows.Forms.CheckBox();
            this.label2 = new System.Windows.Forms.Label();
            this.comboBox_sculpture = new System.Windows.Forms.ComboBox();
            this.textbox_pName = new System.Windows.Forms.TextBox();
            this.comboBox_method = new System.Windows.Forms.ComboBox();
            this.label3 = new System.Windows.Forms.Label();
            this.comboBox_mold = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.textbox_qty = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.textbox_part = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label_currentMold
            // 
            this.label_currentMold.AutoSize = true;
            this.label_currentMold.Location = new System.Drawing.Point(97, 138);
            this.label_currentMold.Name = "label_currentMold";
            this.label_currentMold.Size = new System.Drawing.Size(41, 13);
            this.label_currentMold.TabIndex = 50;
            this.label_currentMold.Text = "label10";
            // 
            // textBox_shrink
            // 
            this.textBox_shrink.Location = new System.Drawing.Point(100, 233);
            this.textBox_shrink.Name = "textBox_shrink";
            this.textBox_shrink.Size = new System.Drawing.Size(54, 20);
            this.textBox_shrink.TabIndex = 39;
            this.textBox_shrink.Text = "7";
            // 
            // button_accept
            // 
            this.button_accept.Enabled = false;
            this.button_accept.Location = new System.Drawing.Point(100, 398);
            this.button_accept.Name = "button_accept";
            this.button_accept.Size = new System.Drawing.Size(168, 32);
            this.button_accept.TabIndex = 49;
            this.button_accept.Text = "Accept";
            this.button_accept.UseVisualStyleBackColor = true;
            this.button_accept.Click += new System.EventHandler(this.button_accept_Click);
            // 
            // textbox_pNum
            // 
            this.textbox_pNum.Enabled = false;
            this.textbox_pNum.Location = new System.Drawing.Point(100, 24);
            this.textbox_pNum.Name = "textbox_pNum";
            this.textbox_pNum.Size = new System.Drawing.Size(121, 20);
            this.textbox_pNum.TabIndex = 42;
            // 
            // listBox_drawings
            // 
            this.listBox_drawings.Enabled = false;
            this.listBox_drawings.FormattingEnabled = true;
            this.listBox_drawings.Location = new System.Drawing.Point(100, 297);
            this.listBox_drawings.Name = "listBox_drawings";
            this.listBox_drawings.Size = new System.Drawing.Size(168, 82);
            this.listBox_drawings.TabIndex = 48;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(10, 57);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(48, 13);
            this.label1.TabIndex = 36;
            this.label1.Text = "P-Name:";
            // 
            // checkBox_cncSculpt
            // 
            this.checkBox_cncSculpt.AutoSize = true;
            this.checkBox_cncSculpt.Location = new System.Drawing.Point(172, 198);
            this.checkBox_cncSculpt.Name = "checkBox_cncSculpt";
            this.checkBox_cncSculpt.Size = new System.Drawing.Size(96, 17);
            this.checkBox_cncSculpt.TabIndex = 47;
            this.checkBox_cncSculpt.Text = "CNC Sculpture";
            this.checkBox_cncSculpt.UseVisualStyleBackColor = true;
            this.checkBox_cncSculpt.Visible = false;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 31);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(57, 13);
            this.label2.TabIndex = 29;
            this.label2.Text = "P-Number:";
            // 
            // comboBox_sculpture
            // 
            this.comboBox_sculpture.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox_sculpture.FormattingEnabled = true;
            this.comboBox_sculpture.Items.AddRange(new object[] {
            "Yes",
            "No"});
            this.comboBox_sculpture.Location = new System.Drawing.Point(100, 194);
            this.comboBox_sculpture.Name = "comboBox_sculpture";
            this.comboBox_sculpture.Size = new System.Drawing.Size(66, 21);
            this.comboBox_sculpture.TabIndex = 46;
            this.comboBox_sculpture.SelectedIndexChanged += new System.EventHandler(this.comboBox_sculpture_SelectedIndexChanged);
            // 
            // textbox_pName
            // 
            this.textbox_pName.Enabled = false;
            this.textbox_pName.Location = new System.Drawing.Point(100, 54);
            this.textbox_pName.Name = "textbox_pName";
            this.textbox_pName.Size = new System.Drawing.Size(121, 20);
            this.textbox_pName.TabIndex = 40;
            // 
            // comboBox_method
            // 
            this.comboBox_method.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox_method.FormattingEnabled = true;
            this.comboBox_method.Items.AddRange(new object[] {
            "CNC",
            "WIRE",
            "TRAD"});
            this.comboBox_method.Location = new System.Drawing.Point(100, 167);
            this.comboBox_method.Name = "comboBox_method";
            this.comboBox_method.Size = new System.Drawing.Size(121, 21);
            this.comboBox_method.TabIndex = 45;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(233, 85);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(78, 13);
            this.label3.TabIndex = 30;
            this.label3.Text = "Part Extension:";
            // 
            // comboBox_mold
            // 
            this.comboBox_mold.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox_mold.FormattingEnabled = true;
            this.comboBox_mold.Location = new System.Drawing.Point(100, 101);
            this.comboBox_mold.Name = "comboBox_mold";
            this.comboBox_mold.Size = new System.Drawing.Size(121, 21);
            this.comboBox_mold.TabIndex = 44;
            this.comboBox_mold.SelectedIndexChanged += new System.EventHandler(this.comboBox_mold_SelectedIndexChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 104);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(55, 13);
            this.label4.TabIndex = 31;
            this.label4.Text = "Use Mold:";
            // 
            // textbox_qty
            // 
            this.textbox_qty.Enabled = false;
            this.textbox_qty.Location = new System.Drawing.Point(100, 271);
            this.textbox_qty.Name = "textbox_qty";
            this.textbox_qty.Size = new System.Drawing.Size(54, 20);
            this.textbox_qty.TabIndex = 43;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(10, 138);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(43, 13);
            this.label5.TabIndex = 32;
            this.label5.Text = "Part ID:";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(10, 297);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(54, 13);
            this.label10.TabIndex = 34;
            this.label10.Text = "Drawings:";
            // 
            // textbox_part
            // 
            this.textbox_part.Location = new System.Drawing.Point(236, 101);
            this.textbox_part.Name = "textbox_part";
            this.textbox_part.Size = new System.Drawing.Size(49, 20);
            this.textbox_part.TabIndex = 41;
            this.textbox_part.Text = "0";
            this.textbox_part.TextChanged += new System.EventHandler(this.textbox_part_TextChanged);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(10, 274);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(49, 13);
            this.label9.TabIndex = 35;
            this.label9.Text = "Quantity:";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(12, 170);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(46, 13);
            this.label6.TabIndex = 33;
            this.label6.Text = "Method:";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(10, 236);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(75, 13);
            this.label7.TabIndex = 38;
            this.label7.Text = "Shrinkage (%):";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(12, 197);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(55, 13);
            this.label8.TabIndex = 37;
            this.label8.Text = "Sculpture:";
            // 
            // Stock
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(325, 469);
            this.Controls.Add(this.label_currentMold);
            this.Controls.Add(this.textBox_shrink);
            this.Controls.Add(this.button_accept);
            this.Controls.Add(this.textbox_pNum);
            this.Controls.Add(this.listBox_drawings);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.checkBox_cncSculpt);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.comboBox_sculpture);
            this.Controls.Add(this.textbox_pName);
            this.Controls.Add(this.comboBox_method);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.comboBox_mold);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.textbox_qty);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.textbox_part);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.label8);
            this.Name = "Stock";
            this.Text = "Stock";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label_currentMold;
        private System.Windows.Forms.TextBox textBox_shrink;
        private System.Windows.Forms.Button button_accept;
        private System.Windows.Forms.TextBox textbox_pNum;
        private System.Windows.Forms.ListBox listBox_drawings;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.CheckBox checkBox_cncSculpt;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox comboBox_sculpture;
        private System.Windows.Forms.TextBox textbox_pName;
        private System.Windows.Forms.ComboBox comboBox_method;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ComboBox comboBox_mold;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox textbox_qty;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox textbox_part;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label8;
    }
}