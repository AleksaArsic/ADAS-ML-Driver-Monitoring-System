using System;
using System.Windows.Forms;
using System.IO;
using System.Collections.Generic;
using System.Drawing;

namespace CaptureLabel
{

    public partial class CaptureLabel : Form
    {

        //private Utilities utilities = new Utilities();

        private string imageFolder = "";
        private List<string> imageLocation;

        private int currentImageIndex = 0;

        // The image's original size.
        private int ImageWidth, ImageHeight;

        // The current scale.
        private float ImageScale = 1.0f;

        public CaptureLabel()
        {
            InitializeComponent();
        }

        private void CaptureLabel_Load(object sender, EventArgs e)
        {
            //this.MouseWheel += new MouseEventHandler(picImage_MouseWheel);
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
                    imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                    //saveImageDimensions();
                    resetImagePanelSize();
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

                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                //saveImageDimensions();
                resetImagePanelSize();
            }
        }

        private void imagePanel_MouseWheel(object sender, MouseEventArgs e)
        {
            
            if (!imagePanel.ClientRectangle.Contains(e.Location)) return;

            // The amount by which we adjust scale per wheel click.
            // 10% per 120 units of delta
            const float scale_per_delta = 0.1f / 120;

            // Update the drawing based upon the mouse wheel scrolling.
            ImageScale += (e.Delta * scale_per_delta);
            if (ImageScale < Constants.imageScaleMin) ImageScale = Constants.imageScaleMin;
            if (ImageScale > Constants.imageScaleMax) ImageScale = Constants.imageScaleMax;

            // Size the image.
            imagePanel.Size = new Size(
                (int)(ImageWidth * ImageScale),
                (int)(ImageHeight * ImageScale));

            // Re-center picturebox
            if (ImageScale > Constants.imageScaleMin && ImageScale < Constants.imageScaleMax)
            {
                imagePanel.Top = (int)(e.Y - ImageScale * (e.Y - groupBox2.Top));
                imagePanel.Left = (int)(e.X - ImageScale * (e.X - groupBox2.Left));
            }
            else if(ImageScale <= Constants.imageScaleMin)
                resetImagePanelSize();
        }

        private void imagePathTB_TextChanged(object sender, EventArgs e)
        {
            imageFolder = imagePathTB.Text;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                try
                {
                    // get list of everything in folder passed to imageFolder
                    imageLocation = new List<string>(Directory.GetFiles(imageFolder));
                }
                catch(ArgumentException)
                {
                    MessageBox.Show(Constants.pathExceptionMsg, Constants.errorCaption);
                    return;
                }
                // Parse list of image locations to contain only image locations
                imageLocation = Utilities.parseImagesToList(imageLocation);

                if (imageLocation.Count > 0)
                {
                    imagePanel.BackgroundImage = Image.FromFile(imageLocation[0]);
                    currentImageIndex = 0;

                    saveImageDimensions();
                }
            }
            catch (IOException)
            {
                MessageBox.Show(Constants.pathExceptionMsg, Constants.errorCaption);
                return;
            }       
        }

        private void saveImageDimensions()
        {
            ImageWidth = imagePanel.Width;
            ImageHeight = imagePanel.Height;
        }


        private void resetImagePanelSize()
        {
            imagePanel.Size = new Size(
                (int)(Constants.pictureBoxSize[0]),
                (int)(Constants.pictureBoxSize[1]));

            imagePanel.Location = new Point(
                    this.groupBox2.Width / 2 - imagePanel.Size.Width / 2,
                    this.groupBox2.Height / 2 - imagePanel.Size.Height / 2);
        }

    }
}
