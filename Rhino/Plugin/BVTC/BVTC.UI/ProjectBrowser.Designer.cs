namespace BVTC.UI
{
    partial class ProjectBrowser
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
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.label_pnum = new System.Windows.Forms.Label();
            this.label_pName = new System.Windows.Forms.Label();
            this.button_accept = new System.Windows.Forms.Button();
            this.listBox_pNameResults = new System.Windows.Forms.ListBox();
            this.textBox_pNameInput = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(18, 24);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(122, 13);
            this.label2.TabIndex = 13;
            this.label2.Text = "Start typing project here:";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(18, 67);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(91, 13);
            this.label1.TabIndex = 12;
            this.label1.Text = "Click your project:";
            // 
            // label_pnum
            // 
            this.label_pnum.AutoSize = true;
            this.label_pnum.Font = new System.Drawing.Font("Microsoft Sans Serif", 13F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_pnum.Location = new System.Drawing.Point(17, 164);
            this.label_pnum.Name = "label_pnum";
            this.label_pnum.Size = new System.Drawing.Size(200, 22);
            this.label_pnum.TabIndex = 11;
            this.label_pnum.Text = "defaultdfasfdsadfasdfas";
            this.label_pnum.Visible = false;
            // 
            // label_pName
            // 
            this.label_pName.AutoSize = true;
            this.label_pName.Font = new System.Drawing.Font("Microsoft Sans Serif", 13F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_pName.Location = new System.Drawing.Point(17, 142);
            this.label_pName.Name = "label_pName";
            this.label_pName.Size = new System.Drawing.Size(200, 22);
            this.label_pName.TabIndex = 10;
            this.label_pName.Text = "defaultdfasfdsadfasdfas";
            this.label_pName.Visible = false;
            // 
            // button_accept
            // 
            this.button_accept.Enabled = false;
            this.button_accept.Location = new System.Drawing.Point(206, 189);
            this.button_accept.Name = "button_accept";
            this.button_accept.Size = new System.Drawing.Size(77, 31);
            this.button_accept.TabIndex = 9;
            this.button_accept.Text = "Accept";
            this.button_accept.UseVisualStyleBackColor = true;
            this.button_accept.Click += new System.EventHandler(this.button_accept_Click);
            // 
            // listBox_pNameResults
            // 
            this.listBox_pNameResults.FormattingEnabled = true;
            this.listBox_pNameResults.Location = new System.Drawing.Point(21, 83);
            this.listBox_pNameResults.Name = "listBox_pNameResults";
            this.listBox_pNameResults.Size = new System.Drawing.Size(262, 56);
            this.listBox_pNameResults.TabIndex = 8;
            this.listBox_pNameResults.SelectedValueChanged += new System.EventHandler(this.listBox_pNameResults_SelectedValueChanged);
            // 
            // textBox_pNameInput
            // 
            this.textBox_pNameInput.Location = new System.Drawing.Point(21, 40);
            this.textBox_pNameInput.Name = "textBox_pNameInput";
            this.textBox_pNameInput.Size = new System.Drawing.Size(262, 20);
            this.textBox_pNameInput.TabIndex = 7;
            this.textBox_pNameInput.TextChanged += new System.EventHandler(this.textBox_pNameInput_TextChanged);
            // 
            // ProjectBrowser
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(296, 243);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.label_pnum);
            this.Controls.Add(this.label_pName);
            this.Controls.Add(this.button_accept);
            this.Controls.Add(this.listBox_pNameResults);
            this.Controls.Add(this.textBox_pNameInput);
            this.Name = "ProjectBrowser";
            this.Text = "ProjectBrowser";
            this.Load += new System.EventHandler(this.ProjectBrowser_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label_pnum;
        private System.Windows.Forms.Label label_pName;
        private System.Windows.Forms.Button button_accept;
        private System.Windows.Forms.ListBox listBox_pNameResults;
        private System.Windows.Forms.TextBox textBox_pNameInput;
    }
}