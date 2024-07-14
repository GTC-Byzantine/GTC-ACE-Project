using System.Timers;

namespace xmsx
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            e.Cancel = true;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.Left = new Random().Next(0, Screen.PrimaryScreen.Bounds.Width - this.Size.Width);
            this.Top = new Random().Next(0, Screen.PrimaryScreen.Bounds.Height - this.Size.Height);
        }
    }
}
