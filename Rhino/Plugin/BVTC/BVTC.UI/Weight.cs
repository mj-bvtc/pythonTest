using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BVTC.UI
{
    public partial class Weight : Form
    {
        public double preKilnWeight { get; set; }
        public double postKilnWeight { get; set; }
        public double shippedWeight { get; set; }

        public Weight()
        {
            setup();
        }

        public Weight(double batched, double fired, double shipped)
        {
            setup();

            this.batchedLabel.Text = string.Format("~Est. {0} lbs.", Math.Round(batched));
            this.firedLabel.Text = string.Format("~Est. {0} lbs.", Math.Round(fired));
            this.shippedLabel.Text = string.Format("~Est. {0} lbs.", Math.Round(shipped));
            
        }

        public void setup()
        {
            this.preKilnWeight = 0;
            this.postKilnWeight = 0;
            this.shippedWeight = 0;

            InitializeComponent();
        }

        private void shipped_TextChanged(object sender, EventArgs e)
        {
            TextBox c = (TextBox)sender;
            double test;
            if (Double.TryParse(c.Text, out test))
            {
                this.shippedWeight = test;
            }
            else
            {
                SuspendLayout();
                this.shipped.Text = "";
                this.shippedWeight = 0;
                ResumeLayout();
            }

        }

        private void postKiln_TextChanged(object sender, EventArgs e)
        {
            TextBox c = (TextBox)sender;
            double test;
            if (Double.TryParse(c.Text, out test))
            {
                this.postKilnWeight = test;
            }
            else
            {
                SuspendLayout();
                this.postKiln.Text = "";
                this.postKilnWeight = 0;
                ResumeLayout();
            }
        }

        private void preKiln_TextChanged(object sender, EventArgs e)
        {
            TextBox c = (TextBox)sender;
            double test;
            if (Double.TryParse(c.Text, out test))
            {
                this.preKilnWeight = test;
            }
            else
            {
                SuspendLayout();
                this.preKiln.Text = "";
                this.preKilnWeight = 0;
                ResumeLayout();
            }
        }
    }
}
