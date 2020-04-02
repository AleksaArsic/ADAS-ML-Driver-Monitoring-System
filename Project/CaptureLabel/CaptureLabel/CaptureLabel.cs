using System;
using System.Windows.Forms;
using System.IO;
using System.Collections.Generic;
using System.Drawing;

namespace CaptureLabel
{

    public partial class CaptureLabel : Form
    {

        private Utilities utilities = new Utilities();

        private string imageFolder = "";
        private List<string> imageLocation;

        private int currentImageIndex = 0;

        public CaptureLabel()
        {
            InitializeComponent();
        }

        private void importToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void CaptureLabel_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.PageDown)
            {
                currentImageIndex++;

                if(currentImageIndex < imageLocation.Count)
                {
                    imageViewPB.Image = Image.FromFile(imageLocation[currentImageIndex]);
                }
                else
                {
                    currentImageIndex = imageLocation.Count - 1;
                }
            }
            if(e.KeyCode == Keys.PageUp)
            {
                currentImageIndex--;

                if (currentImageIndex < 0)
                    currentImageIndex = 0;

                imageViewPB.Image = Image.FromFile(imageLocation[currentImageIndex]);
            }
        }

        private void imagePathTB_TextChanged(object sender, EventArgs e)
        {
            imageFolder = imagePathTB.Text;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //imageViewPB.Image = Image.FromFile(imageFolder);
            imageLocation = new List<string>(Directory.GetFiles(imageFolder));

            imageLocation = utilities.parseImagesToList(imageLocation);

            if (imageLocation.Count > 0)
            {
                imageViewPB.Image = Image.FromFile(imageLocation[0]);
                currentImageIndex = 0;
            }
        }

        

    }
}
