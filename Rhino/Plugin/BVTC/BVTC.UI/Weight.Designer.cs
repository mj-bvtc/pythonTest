namespace BVTC.UI
{
    partial class Weight
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
            this.button1 = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.shipped = new System.Windows.Forms.TextBox();
            this.postKiln = new System.Windows.Forms.TextBox();
            this.preKiln = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.batchedLabel = new System.Windows.Forms.Label();
            this.firedLabel = new System.Windows.Forms.Label();
            this.shippedLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.button1.Location = new System.Drawing.Point(228, 86);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 0;
            this.button1.Text = "Okay";
            this.button1.UseVisualStyleBackColor = true;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(13, 13);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(113, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Actual Pre-Kiln Weight";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(13, 37);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(118, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Actual Post-Kiln Weight";
            // 
            // shipped
            // 
            this.shipped.Location = new System.Drawing.Point(145, 6);
            this.shipped.Name = "shipped";
            this.shipped.Size = new System.Drawing.Size(100, 20);
            this.shipped.TabIndex = 3;
            this.shipped.WordWrap = false;
            this.shipped.TextChanged += new System.EventHandler(this.shipped_TextChanged);
            // 
            // postKiln
            // 
            this.postKiln.Location = new System.Drawing.Point(145, 32);
            this.postKiln.Name = "postKiln";
            this.postKiln.Size = new System.Drawing.Size(100, 20);
            this.postKiln.TabIndex = 4;
            this.postKiln.TextChanged += new System.EventHandler(this.postKiln_TextChanged);
            // 
            // preKiln
            // 
            this.preKiln.Location = new System.Drawing.Point(145, 60);
            this.preKiln.Name = "preKiln";
            this.preKiln.Size = new System.Drawing.Size(100, 20);
            this.preKiln.TabIndex = 5;
            this.preKiln.TextChanged += new System.EventHandler(this.preKiln_TextChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(13, 63);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(116, 13);
            this.label3.TabIndex = 6;
            this.label3.Text = "Actual Shipped Weight";
            // 
            // batchedLabel
            // 
            this.batchedLabel.AutoSize = true;
            this.batchedLabel.Location = new System.Drawing.Point(251, 13);
            this.batchedLabel.Name = "batchedLabel";
            this.batchedLabel.Size = new System.Drawing.Size(35, 13);
            this.batchedLabel.TabIndex = 7;
            this.batchedLabel.Text = "label4";
            // 
            // firedLabel
            // 
            this.firedLabel.AutoSize = true;
            this.firedLabel.Location = new System.Drawing.Point(251, 37);
            this.firedLabel.Name = "firedLabel";
            this.firedLabel.Size = new System.Drawing.Size(35, 13);
            this.firedLabel.TabIndex = 8;
            this.firedLabel.Text = "label5";
            // 
            // shippedLabel
            // 
            this.shippedLabel.AutoSize = true;
            this.shippedLabel.Location = new System.Drawing.Point(251, 63);
            this.shippedLabel.Name = "shippedLabel";
            this.shippedLabel.Size = new System.Drawing.Size(35, 13);
            this.shippedLabel.TabIndex = 9;
            this.shippedLabel.Text = "label6";
            // 
            // Weight
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(315, 125);
            this.Controls.Add(this.shippedLabel);
            this.Controls.Add(this.firedLabel);
            this.Controls.Add(this.batchedLabel);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.preKiln);
            this.Controls.Add(this.postKiln);
            this.Controls.Add(this.shipped);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.button1);
            this.Name = "Weight";
            this.Text = "Weight";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox shipped;
        private System.Windows.Forms.TextBox postKiln;
        private System.Windows.Forms.TextBox preKiln;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label batchedLabel;
        private System.Windows.Forms.Label firedLabel;
        private System.Windows.Forms.Label shippedLabel;
    }
}