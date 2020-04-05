using System;
using System.Windows.Forms;
using System.IO;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Reflection;
using CsvHelper;
using System.Text;
using System.Linq;

namespace CaptureLabel
{

    public partial class CaptureLabel : Form
    {
        private string imageFolder = "";
        private string csvPath = "";
        private string csvFileName = "newCsv.csv";
        private List<string> imageLocation = new List<string>();
        private List<string> imageNames = new List<string>();
        private List<double> imageResizeFactor = new List<double>();
        private List<double> imagePadX = new List<double>();
        private List<double> imagePadY = new List<double>();
        private int currentImageIndex = 0;

        // Rectangle labelers variables
        private RectangleContainer rectangles = new RectangleContainer();
        private Tuple<bool, int> currentlyInFocus;
        private bool someoneIsInFocus = false;

        // Coordinates of all rectangles in one *** picture set ***
        private CoordinatesContainer coordinatesList = new CoordinatesContainer();
        private CoordinatesContainer realCoordinatesList = new CoordinatesContainer();
        private bool isLoaded = false;

        // mouse position
        private int mouseX = 0;
        private int mouseY = 0;

        public CaptureLabel()
        {
            InitializeComponent();
            typeof(Panel).InvokeMember("DoubleBuffered", BindingFlags.SetProperty
               | BindingFlags.Instance | BindingFlags.NonPublic, null,
               imagePanel, new object[] { true });
            typeof(Panel).InvokeMember("DoubleBuffered", BindingFlags.SetProperty
               | BindingFlags.Instance | BindingFlags.NonPublic, null,
               ZoomViewP, new object[] { true });
        }

        private void CaptureLabel_Load(object sender, EventArgs e)
        {
            //leftUp.MouseLeftButtonDown += rectangle_MouseLeftButtonDown;
        }

        private void importToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void CaptureLabel_KeyDown(object sender, KeyEventArgs e)
        { 
            // reset state of rectangles
            if(e.KeyCode == Keys.PageUp || e.KeyCode == Keys.PageDown)
            {
                // save all rectangles coordinates
                saveCoordinates();

                if (e.KeyCode == Keys.PageDown)
                    scrollDown();
                if (e.KeyCode == Keys.PageUp)
                    scrollUp();

                if (!isLoaded)
                    rectangles.resetCoordinates();

                rectangles.resetFocusList();
                someoneIsInFocus = false;
                imagePanel.Refresh();
               
            }

            // paste previous picture rectangles to current picture
            if (e.KeyCode == Keys.X && currentImageIndex >= 1)
            {
                //List<int> previosCoordinates = coordinatesList.getRow(currentImageIndex - 1);
                //rectangles.setAllRectCoordinates(previosCoordinates);
                loadCoordinates(currentImageIndex - 1);
                imagePanel.Refresh();
            }

            // move rectangles with keyboard
            if (someoneIsInFocus)
            {
                if (e.KeyCode == Keys.Left)
                {
                    rectangles.addToFocused(-1, 0);
                    imagePanel.Refresh();
                    setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Right)
                {
                    rectangles.addToFocused(1, 0);
                    imagePanel.Refresh();
                    setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Down)
                {
                    rectangles.addToFocused(0, 1);
                    imagePanel.Refresh();
                    setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Up)
                {
                    rectangles.addToFocused(0, -1);
                    imagePanel.Refresh();
                    setZoomView(mouseX, mouseY);
                }
            }

            if(Array.Exists(Constants.focusShortcuts, element => element == e.KeyCode))
            {
                //Console.WriteLine(e.KeyCode.ToString());
                rectangles.resetFocusList();
                rectangles.setFocus(Array.IndexOf(Constants.focusShortcuts, e.KeyCode));
                someoneIsInFocus = true;
                imagePanel.Refresh();
            }


            if (e.KeyCode == Keys.Z)
                writeToCSV();
        }


        private void imagePanel_MouseDown(object sender, MouseEventArgs e)
        {
            if (!imagePanel.ClientRectangle.Contains(e.Location)) return;
            
            if(e.Button == MouseButtons.Left)
            {
                mouseX = Cursor.Position.X;
                mouseY = Cursor.Position.Y;

                setZoomView(mouseX, mouseY);

                // set rect in focus
                currentlyInFocus = rectangles.contains(e.Location);
                if (currentlyInFocus.Item1)
                {
                    rectangles.resetFocusList();
                    someoneIsInFocus = false;
                    rectangles.setFocus(currentlyInFocus.Item2);
                    imagePanel.Refresh();
                    someoneIsInFocus = !someoneIsInFocus;
                }
            }

        }

        private void imagePanel_MouseUp(object sender, MouseEventArgs e)
        {
            // reset focus
            /*
            if (someoneIsInFocus)
            {
                rectangles.setFocus(currentlyInFocus.Item2);
                imagePanel.Refresh();
                someoneIsInFocus = false;
            }
            */
            //Focus();

        }

        private void imagePanel_MouseMove(object sender, MouseEventArgs e)
        {
            Rectangle rectInFocus = rectangles.findInFocus();

            if (e.Button == MouseButtons.Left && someoneIsInFocus && rectInFocus.Contains(e.Location))
            {
                // Increment rectangle-location by mouse-location delta.
                int x = e.X - rectInFocus.X;
                int y = e.Y - rectInFocus.Y;

                rectangles.addToFocused(x, y);

                imagePanel.Refresh();
            }
            
        }


        private void imagePanel_MouseWheel(object sender, MouseEventArgs e)
        {
            
            if (!imagePanel.ClientRectangle.Contains(e.Location)) return;

            saveCoordinates();

            if(e.Delta > 0)
            {
                // user scrolled up
                scrollUp();
            }
            else
            {
                // user scrolled down
                scrollDown();
            }

            if (!isLoaded)
                rectangles.resetCoordinates();
            rectangles.resetFocusList();
            someoneIsInFocus = false;
            imagePanel.Refresh();


            /*
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

         */
        }
        
        private void imagePanel_Paint(object sender, PaintEventArgs e)
        {
            Rectangle[] rects = rectangles.getRectangles();
            int inFocus = rectangles.inFocusIndex();

            for(int i = 0; i < rects.Length; i++)
            {
                if(inFocus == i)
                    e.Graphics.FillRectangle(new SolidBrush(Color.Red), rects[i]);
                else
                    e.Graphics.DrawRectangle(new Pen(Color.Red), rects[i]);
            }

        }

        private void imagePathTB_TextChanged(object sender, EventArgs e)
        {
            imageFolder = imagePathTB.Text;
        }

        private void csvPathTB_TextChanged(object sender, EventArgs e)
        {
            csvPath = csvPathTB.Text;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                try
                {
                    // get list of everything in folder passed to imageFolder
                    imageLocation = new List<string>(Directory.GetFiles(imageFolder));
                    //csvFileName = Path.GetFileName(Path.GetDirectoryName(imageFolder));
                    csvFileName = new DirectoryInfo(imageFolder).Name;
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

                    foreach(string name in imageLocation)
                        imageNames.Add(Path.GetFileNameWithoutExtension(name));

                    // check for existing .csv file
                    if(!String.IsNullOrEmpty(csvPath))
                    {
                        // read and load coordinates from .csv
                        realCoordinatesList = readFromCSV(csvPath);

                        for (int i = 0; i < imageNames.Count; i++)
                        {
                            imagePanel.BackgroundImage = Image.FromFile(imageLocation[i]);
                            calculateResizeFactor(i);
                            imagePanel.BackgroundImage.Dispose();
                        }

                        List<int> singleRow;
                        // set rectangle coordinates based on real one read from .csv file
                        for (int i = 0; i < realCoordinatesList.getSize(); i++)
                        {
                            singleRow = realCoordinatesList.getRow(i);
                            List<int> tempCord = new List<int>(calculateRectangleCoordinates(singleRow, i));
                            coordinatesList.addRow(tempCord);
                            singleRow.Clear();
                        }

                        imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                        loadCoordinates(currentImageIndex);

                        imagePanel.Refresh();
                    }
                }
            }
            catch (IOException)
            {
                MessageBox.Show(Constants.pathExceptionMsg, Constants.errorCaption);
                return;
            }

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

        private void setZoomView(int xCoordinate, int yCoordinate)
        {
            // Zoom View copy
            Bitmap screenshot = Utilities.CaptureScreenShot();

            Cursor = new Cursor(Cursor.Current.Handle);

            Bitmap portionOf = screenshot.Clone(new Rectangle(xCoordinate - 25, yCoordinate - 25, 50, 50), PixelFormat.Format32bppRgb);
            Bitmap zoomedPortion = new Bitmap(portionOf, new Size(400, 400));

            if (ZoomViewP.BackgroundImage != null)
            {
                ZoomViewP.BackgroundImage.Dispose();
                screenshot.Dispose();
                portionOf.Dispose();
            }
            ZoomViewP.BackgroundImage = zoomedPortion;
        }

        public void scrollDown()
        {
            currentImageIndex++;

            if (currentImageIndex < imageLocation.Count)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                //imagePanel.ClientRectangle.Inflate(new Size(imagePanel.Width, imagePanel.Height));
                resetImagePanelSize();
                isLoaded = loadCoordinates(currentImageIndex);
            }
            else
            {
                currentImageIndex = imageLocation.Count - 1;
            }
        }

        public void scrollUp()
        {
            currentImageIndex--;

            if (currentImageIndex < 0)
                currentImageIndex = 0;

            if (imageLocation.Count > 0)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                resetImagePanelSize();
                isLoaded = loadCoordinates(currentImageIndex);
            }
        }

        public void saveCoordinates()
        {
            // save all rectangles coordinates
            List<int> coordinates = rectangles.getAllRectCoordinates();

            double resizeFactor = 0;

            try
            {
                resizeFactor = imageResizeFactor[currentImageIndex];
            }
            catch(ArgumentOutOfRangeException)
            {
                calculateResizeFactor(currentImageIndex);
                resizeFactor = imageResizeFactor[currentImageIndex];
            }

            // calculate real coordinates
            if (coordinatesList.getRow(currentImageIndex) == null)
            {
                coordinatesList.addRow(coordinates);
                realCoordinatesList.addRow(calculateRealCoordinates(coordinates));
            }
            else
            {
                coordinatesList.replaceRow(coordinates, currentImageIndex);
                realCoordinatesList.replaceRow(calculateRealCoordinates(coordinates), currentImageIndex);
            }
        }

        public bool loadCoordinates(int index)
        {
            if (index >= realCoordinatesList.getSize())
                return false;
            /*
            List<int> singleRow;
            // set rectangle coordinates based on real one read from .csv file
            for (int i = 0; i < realCoordinatesList.getSize(); i++)
            {
                singleRow = realCoordinatesList.getRow(i);
                List<int> tempCord = new List<int>(calculateRectangleCoordinates(singleRow));
                coordinatesList.addRow(tempCord);
                singleRow.Clear();
            }
            */
            /*
            //if (index > coordinatesList.getSize())
            //{
                calculateResizeFactor(index);

                List<int> singleRow = calculateRectangleCoordinates(realCoordinatesList.getRow(index));

                if (singleRow != null)
                {
                    coordinatesList.replaceRow(singleRow, index);
                    rectangles.setAllRectCoordinates(singleRow);
                    return true;
                }
            //}
            */
            
            List<int> singleRow = coordinatesList.getRow(index);
            if (singleRow != null)
            {
                rectangles.setAllRectCoordinates(singleRow);
                return true;
            }
            
            
            return false;
        }

        public void calculateResizeFactor(int index)
        {
            if (imagePanel.BackgroundImage == null)
                return;

            int realW = imagePanel.BackgroundImage.Width;
            int realH = imagePanel.BackgroundImage.Height;
            int currentW = imagePanel.ClientRectangle.Width;
            int currentH = imagePanel.ClientRectangle.Height;
            double wFactor = (double)currentW / realW;
            double hFactor = (double)currentH / realH;

            double resizeFactor = Math.Min(wFactor, hFactor);

            double padX = resizeFactor == wFactor ? 0 : (currentW - (resizeFactor * realW)) / 2;
            double padY = resizeFactor == hFactor ? 0 : (currentH - (resizeFactor * realH)) / 2;

            if (index < imageResizeFactor.Count)
            {
                imageResizeFactor[index] = resizeFactor;
                imagePadX[index] = padX;
                imagePadY[index] = padY;
            }
            else
            {
                imageResizeFactor.Add(resizeFactor);
                imagePadX.Add(padX);
                imagePadY.Add(padY);
            }
        }

        public List<int> calculateRealCoordinates(List<int> l)
        {

            List<int> realCoordinates = new List<int>();

            int tempX = 0;
            int tempY = 0;
            for (int i = 0; i < l.Count; i += 2)
            {
                tempX = (int)((l[i] - imagePadX[currentImageIndex]) / imageResizeFactor[currentImageIndex]);
                tempY = (int)((l[i + 1] - imagePadY[currentImageIndex]) / imageResizeFactor[currentImageIndex]);
                realCoordinates.Add(tempX);
                realCoordinates.Add(tempY);
            }

            return realCoordinates;
        }

        public List<int> calculateRectangleCoordinates(List<int> l, int index)
        {
            List<int> rectCoordinates = new List<int>();

            int tempX = 0;
            int tempY = 0;
            for (int i = 0; i < l.Count; i += 2)
            {
                tempX = (int)((l[i] * imageResizeFactor[index]) + imagePadX[index]);
                tempY = (int)((l[i + 1] * imageResizeFactor[index]) + imagePadY[index]);
                rectCoordinates.Add(tempX);
                rectCoordinates.Add(tempY);
            }

            return rectCoordinates;
        }

        private void writeToCSV()
        {
            string csvPath = Path.Combine(new string[] { imageFolder, csvFileName }) + ".csv";
            TextWriter writer = new StreamWriter(@csvPath, false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            csv.WriteField("");

            foreach (string s in RectangleContainer.names)
            {
                csv.WriteField(s);
                csv.WriteField("");
            }

            csv.NextRecord();

            csv.WriteField("Picture:");

            for (int i = 0; i < rectangles.getSize(); i++)
            {
                csv.WriteField("(x,");
                csv.WriteField("y)");
            }

            csv.NextRecord();

            for(int i = 0; i < realCoordinatesList.getSize(); i++)
            {
                csv.WriteField(imageNames[i]);

                foreach(int value in realCoordinatesList.getRow(i))
                {
                    csv.WriteField(value);
                }

                csv.NextRecord();
            }
            
            writer.Close();
        }

        public CoordinatesContainer readFromCSV(string path)
        {
            
            CoordinatesContainer result = new CoordinatesContainer();
            List<int> singleRow = new List<int>();
            int value;
            using (TextReader fileReader = File.OpenText(path))
            {
                var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                csv.Configuration.HasHeaderRecord = false;

                csv.Read();
                csv.Read();

                while (csv.Read())
                {
                    for (int i = 1; csv.TryGetField<int>(i, out value); i++)
                    {
                        singleRow.Add(value);
                    }
                    List<int> temp = new List<int>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }
                
            }
            return result;
            
            /*
            var parser = new CsvParser(textReader);
            while (true)
            {
                string[] row = parser.Read();
                if (row == null)
                {
                    break;
                }
            }
            */
        }

    }
}
