using System;
using System.Windows.Forms;
using System.IO;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Reflection;

namespace CaptureLabel
{

    public partial class CaptureLabel : Form
    {
        public static string imageFolder = "";
        public static string csvPath = "";
        public static string csvFileName = "newCsv.csv";
        public static string saveDirectory = "";
        public static string exportDirectory = "";
        public static string exportMinMaxDirectory = "";
        private List<string> imageLocation = new List<string>();
        private List<string> imageNames = new List<string>();
        private List<double> imageResizeFactor = new List<double>();
        private List<double> imagePadX = new List<double>();
        private List<double> imagePadY = new List<double>();
        private int currentImageIndex = 0;

        private bool savedAs = false;

        // Rectangle labelers variables
        private RectangleContainer rectangles;
        private Tuple<bool, int> currentlyInFocus;
        private bool someoneIsInFocus = false;

        // Coordinates of all rectangles in one *** picture set ***
        private CoordinatesContainer<int> coordinatesList = new CoordinatesContainer<int>();
        private CoordinatesContainer<int> realCoordinatesList = new CoordinatesContainer<int>();
        private bool isLoaded = false;

        // face mode look angle checkbox values
        // left, right, up, down
        // all zeroes represent center
        private int[] lookAngle = { 0, 0, 0, 0 };
        private CoordinatesContainer<int> lookAngleContainer = new CoordinatesContainer<int>();
        private CoordinatesContainer<int> faceModeSize = new CoordinatesContainer<int>();

        bool loaded = false;

        // mouse position
        private int mouseX = 0;
        private int mouseY = 0;

        private char mode = 'f';
        private bool modeSet = false;

        public CaptureLabel()
        {
            InitializeComponent();
            typeof(Panel).InvokeMember("DoubleBuffered", BindingFlags.SetProperty
               | BindingFlags.Instance | BindingFlags.NonPublic, null,
               imagePanel, new object[] { true });
            /*
            typeof(Panel).InvokeMember("DoubleBuffered", BindingFlags.SetProperty
               | BindingFlags.Instance | BindingFlags.NonPublic, null,
               ZoomViewP, new object[] { true });
            */
            initMode(mode);
        }

        private void CaptureLabel_Load(object sender, EventArgs e)
        {
            //leftUp.MouseLeftButtonDown += rectangle_MouseLeftButtonDown;
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
                    rectangles.resetCoordinates(mode);

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
                    //setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Right)
                {
                    rectangles.addToFocused(1, 0);
                    imagePanel.Refresh();
                    //setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Down)
                {
                    rectangles.addToFocused(0, 1);
                    imagePanel.Refresh();
                    //setZoomView(mouseX, mouseY);
                }
                if (e.KeyCode == Keys.Up)
                {
                    rectangles.addToFocused(0, -1);
                    imagePanel.Refresh();
                    //setZoomView(mouseX, mouseY);
                }
            }

            // Set focus based on keyboard shortcut
            // for face mode this will cause error. 
            // index out of range when setting focus on elements past index 2 
            // in focusShortcuts array

            Keys[] focusShortcuts = (mode == 'e' ? Constants.focusShortcutsE : Constants.focusShortcutsF);

            if (Array.Exists(focusShortcuts, 
                            element => element == e.KeyCode) &&
                            !imagePathTB.Focused && !csvPathTB.Focused)
            {
                rectangles.resetFocusList();
                rectangles.setFocus(Array.IndexOf(focusShortcuts, e.KeyCode));
                someoneIsInFocus = true;
                imagePanel.Refresh();
            }


            /*
            if (e.KeyCode == Keys.Z)
            {
                // correct coordinates only if the face mode is used
                saveCoordinates();
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, Constants.modeFRectScale);
                Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer, faceModeSize);
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, Constants.modeFRectScale, true);
            }
            */
        }


        private void imagePanel_MouseDown(object sender, MouseEventArgs e)
        {
            if (!imagePanel.ClientRectangle.Contains(e.Location)) return;
            
            if(e.Button == MouseButtons.Left)
            {
                mouseX = Cursor.Position.X;
                mouseY = Cursor.Position.Y;

                //setZoomView(mouseX, mouseY);

                // set rect in focus
                currentlyInFocus = rectangles.contains(e.Location);
                if (currentlyInFocus.Item1)
                {
                    rectangles.resetFocusList();
                    //someoneIsInFocus = false;
                    someoneIsInFocus = true;
                    if(someoneIsInFocus)
                        rectangles.setFocus(currentlyInFocus.Item2);
                    imagePanel.Refresh();
                }

                else
                {
                    int inFocus = rectangles.inFocusIndex();
                    Rectangle rectInFocus = rectangles.findInFocus();

                    if(inFocus != -1)
                        rectangles.setRectCoordinates(inFocus, e.X - rectInFocus.Width / 2, e.Y - rectInFocus.Height / 2);

                    imagePanel.Refresh();

                }
            }

        }

        private void imagePanel_MouseUp(object sender, MouseEventArgs e)
        {
            // set focus to image panel 
            if (imagePanel.ClientRectangle.Contains(e.Location))
                imagePanel.Focus();

            if(someoneIsInFocus)
            {
                someoneIsInFocus = false;
                rectangles.resetFocusList();
                imagePanel.Refresh();
            }
            
        }

        private void imagePanel_MouseMove(object sender, MouseEventArgs e)
        {

            if (e.Button == MouseButtons.Left && someoneIsInFocus)// && rectInFocus.Contains(e.Location))
            {
                Rectangle rectInFocus = rectangles.findInFocus();

                // Increment rectangle-location by mouse-location delta.
                int x = e.X - rectInFocus.X - rectInFocus.Width / 2;
                int y = e.Y - rectInFocus.Y - rectInFocus.Height / 2;
                //rect.X = rect.X + e.X - MouseDownLocation.X;
               // rect.Y = rect.Y + e.Y - MouseDownLocation.Y;

                rectangles.addToFocused(x, y);

                imagePanel.Refresh();
            }
            
        }


        private void imagePanel_MouseWheel(object sender, MouseEventArgs e)
        {
            
            if (!imagePanel.ClientRectangle.Contains(e.Location) || imagePanel.BackgroundImage == null) return;

            if(mode == 'f' && Control.ModifierKeys == Keys.Control)
            {
                if (e.Delta > 0)
                    rectangles.addToRectSize(0, Constants.modeFRectDeltaSize, (int)(Constants.modeFRectDeltaSize * Constants.modeFRectScale));
                else
                    rectangles.addToRectSize(0, -Constants.modeFRectDeltaSize, (int)(-Constants.modeFRectDeltaSize * Constants.modeFRectScale));

                imagePanel.Refresh();

                return;
            }


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
                rectangles.resetCoordinates(mode);
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
            if (!loaded)
                return;

            Rectangle[] rects = rectangles.getRectangles();
            int inFocus = rectangles.inFocusIndex();

            for(int i = 0; i < rects.Length; i++)
            {
                if((mode == 'e' && inFocus == i) || (mode == 'f' && i != 0 && inFocus == i))
                    e.Graphics.FillRectangle(new SolidBrush(Color.Red), rects[i]);
                else
                    e.Graphics.DrawRectangle(new Pen(Color.Red), rects[i]);
            }

            if (someoneIsInFocus && mode == 'e')
                inFocusLabel.Text = Constants.inFocusString + " " + Constants.rectangleNameE[rectangles.inFocusIndex()];
            if(someoneIsInFocus && mode == 'f')
                inFocusLabel.Text = Constants.inFocusString + " " + Constants.rectangleNameF[rectangles.inFocusIndex()];

            imagePanel.Focus();
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
            cleanUp();

            initMode(mode);

            try
            {
                
                // get list of everything in folder passed to imageFolder
                imageLocation = new List<string>(Directory.GetFiles(imageFolder));
                //csvFileName = Path.GetFileName(Path.GetDirectoryName(imageFolder));
                csvFileName = new DirectoryInfo(imageFolder).Name;
                
                // Parse list of image locations to contain only image locations
                imageLocation = Utilities.parseImagesToList(imageLocation);

                if (imageLocation.Count > 0)
                {
                    imagePanel.BackgroundImage = Image.FromFile(imageLocation[0]);
                    currentImageIndex = 0;

                    foreach(string name in imageLocation)
                        imageNames.Add(Path.GetFileNameWithoutExtension(name));

                    // check for existing .csv file
                    if(!String.IsNullOrEmpty(csvPath) && csvPath.Contains(".csv"))
                    {
                        // read and load coordinates from .csv
                        realCoordinatesList = Utilities.readFromCSV<int>(csvPath, mode);

                        //if (mode == 'f')
                        lookAngleContainer = Utilities.readLookAngleFromCSV<int>(csvPath);

                        faceModeSize = Utilities.readFaceSizeFromCSV<int>(csvPath);

                        for (int i = 0; i < imageNames.Count; i++)
                        {
                            imagePanel.BackgroundImage = Image.FromFile(imageLocation[i]);
                            calculateResizeFactor(i);
                            imagePanel.BackgroundImage.Dispose();
                        }

                        if (mode == 'f')
                            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);

                        List<int> singleRow;
                        // set rectangle coordinates based on real one read from .csv file
                        for (int i = 0; i < realCoordinatesList.getSize(); i++)
                        {
                            singleRow = realCoordinatesList.getRow(i);
                            coordinatesList.addRow(new List<int>(calculateRectangleCoordinates(singleRow, i)));
                        }

                        imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);

                        loadCoordinates(currentImageIndex);

                        //csvPathTB.ReadOnly = true;

                    }
                    imagePathTB.ReadOnly = true;
                    loaded = true;
                }
            }
            catch (Exception msg)
            {
                imagePathTB.ReadOnly = false;
                MessageBox.Show(msg.Message, Constants.errorCaption, MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            imagePanel.Refresh();
        }

        /*
        private void resetImagePanelSize()
        {
            imagePanel.Size = new Size(
                (int)(Constants.pictureBoxSize[0]),
                (int)(Constants.pictureBoxSize[1]));

            imagePanel.Location = new Point(
                    this.groupBox2.Width / 2 - imagePanel.Size.Width / 2,
                    this.groupBox2.Height / 2 - imagePanel.Size.Height / 2);
        }
        */
        /*
        private void setZoomView(int xCoordinate, int yCoordinate)
        {
            // Zoom View copy
            Bitmap screenshot = Utilities.CaptureScreenShot();

            Cursor = new Cursor(Cursor.Current.Handle);

            Bitmap portionOf = screenshot.Clone(new Rectangle(xCoordinate - 50, yCoordinate - 50, 100, 100), PixelFormat.Format32bppRgb);
            Bitmap zoomedPortion = new Bitmap(portionOf, new Size(400, 400));

            if (ZoomViewP.BackgroundImage != null)
            {
                ZoomViewP.BackgroundImage.Dispose();
                screenshot.Dispose();
                portionOf.Dispose();
            }
            ZoomViewP.BackgroundImage = zoomedPortion;
        }
        */
        private void scrollDown()
        {
            currentImageIndex++;

            if (currentImageIndex < imageLocation.Count)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                //resetImagePanelSize();
                isLoaded = loadCoordinates(currentImageIndex);
                //resetCheckBoxes(new CheckBox[] { leftCB, rightCB, upCB, downCB });
            }
            else
            {
                currentImageIndex = imageLocation.Count - 1;
            }
        }

        private void scrollUp()
        {
            currentImageIndex--;

            if (currentImageIndex < 0)
                currentImageIndex = 0;

            if (imageLocation.Count > 0)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                //resetImagePanelSize();
                isLoaded = loadCoordinates(currentImageIndex);
            }
        }

        private void saveCoordinates()
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

            int faceWidth = (mode == 'f') ? rectangles.getRectangles()[0].Width : (int)(imagePanel.BackgroundImage.Width * imageResizeFactor[currentImageIndex]);
            // calculate real coordinates
            if (coordinatesList.getRow(currentImageIndex) == null)
            {
                lookAngleContainer.addRow(lookAngle.ToList());
                //rectSizeFmode.Add(rectangles.getRectangles()[0].Width);
                faceModeSize.addRow(new List<int> { faceWidth });
                coordinatesList.addRow(coordinates);
                realCoordinatesList.addRow(calculateRealCoordinates(coordinates));
            }
            else
            {
                lookAngleContainer.replaceRow(lookAngle.ToList(), currentImageIndex);
                coordinatesList.replaceRow(coordinates, currentImageIndex);
                realCoordinatesList.replaceRow(calculateRealCoordinates(coordinates), currentImageIndex);
                faceModeSize.replaceRow(new List<int> { faceWidth }, currentImageIndex);
                //rectSizeFmode[currentImageIndex] = rectangles.getRectangles()[0].Width;
            }

            lookAngle = new int[] { 0, 0, 0, 0 };
            setCheckBoxes(new CheckBox[] { leftCB, rightCB, upCB, downCB });
        }

        private bool loadCoordinates(int index)
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
            List<int> faceSize = faceModeSize.getRow(index);
            //List<int> singleRow = calculateRectangleCoordinates(realCoordinatesList.getRow(index), index);
            lookAngle = new int[] { 0, 0, 0, 0 };

            if (singleRow != null)
            {
                rectangles.setAllRectCoordinates(singleRow);
                //rectangles.setRectSize(0, new Size(new Point(rectSizeFmode[currentImageIndex], rectSizeFmode[currentImageIndex])));
                lookAngle = lookAngleContainer.getRow(index).ToArray();

                if (mode == 'f')
                    rectangles.setRectSize(0, new Size(faceSize[0], (int)(faceSize[0] * Constants.modeFRectScale)));

                // set checkboxes
                setCheckBoxes(new CheckBox[] { leftCB, rightCB, upCB, downCB });

                return true;
            }
            
            
            return false;
        }

        private void calculateResizeFactor(int index)
        {
            if (imagePanel.BackgroundImage == null)
                return;

            int realW = imagePanel.BackgroundImage.Width;
            int realH = imagePanel.BackgroundImage.Height;
            int currentW = imagePanel.Width;
            int currentH = imagePanel.Height;
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

        private List<int> calculateRealCoordinates(List<int> l)
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

        private List<int> calculateRectangleCoordinates(List<int> l, int index)
        {
            List<int> rectCoordinates = new List<int>();

            //calculateResizeFactor(index);

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

        private void cleanUp()
        {
            imagePathTB.ReadOnly = false;
            csvPathTB.ReadOnly = false;

            csvFileName = "newCsv.csv";
            
            imageLocation = null;
            imageNames = null;
            imageResizeFactor = null;
            imagePadX = null;
            imagePadY = null;
            rectangles = null;
            coordinatesList = null;
            realCoordinatesList = null;

            faceModeSize = null;
            lookAngleContainer = null;

            currentImageIndex = 0;
            isLoaded = false;
            someoneIsInFocus = false;
            savedAs = false;

            imageLocation = new List<string>();
            imageNames = new List<string>();
            imageResizeFactor = new List<double>();
            imagePadX = new List<double>();
            imagePadY = new List<double>();
            //rectangles = new RectangleContainer();
            coordinatesList = new CoordinatesContainer<int>();
            realCoordinatesList = new CoordinatesContainer<int>();

            faceModeSize = new CoordinatesContainer<int>();
            lookAngleContainer = new CoordinatesContainer<int>();

        }

        private void initMode(char currentMode)
        {
            if (currentMode == 'f')
            {
                rectangles = new RectangleContainer(3, Constants.faceModeStartPos, Constants.faceModeStartSize);
                //lookAngleGB.Visible = true;
            }
            if (currentMode == 'e')
            {
                rectangles = new RectangleContainer();
                //lookAngleGB.Visible = false;
            }
        }

        private void leftCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(leftCB, 0);
            rightCB.Checked = false;
        }

        private void rightCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(rightCB, 1);
            leftCB.Checked = false;
        }

        private void upCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(upCB, 2);
            downCB.Checked = false;
        }

        private void downCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(downCB, 3);
            upCB.Checked = false;
        }

        private void setLookAngle(CheckBox cb, int index)
        {
            lookAngle[index] = cb.Checked ? 1 : 0;
        }

        private void setCheckBoxes(CheckBox[] lookAngleCBs)
        {
            for(int i = 0; i < lookAngleCBs.Length; i++)
            {
                lookAngleCBs[i].Checked = (lookAngle[i] == 1 ? true : false);
            }
        }

        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if(MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
            {
                // save logic
                if (!savedAs)
                    saveAs();
                else
                    save();
            }
            
            loaded = false;
            imagePanel.BackgroundImage = null;
            imagePathTB.Text = "";
            csvPathTB.Text = "";
            cleanUp();
            imagePanel.Refresh();
            
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                if(!savedAs)
                    saveAs();
                else
                    save();
            }
        }

        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // save as logic

            saveAs();
        }

        private void saveAs()
        {
            if (!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "CSV File|*.csv|All files|*.*";
                saveFileDialog.Title = "Save .csv File";
                saveFileDialog.RestoreDirectory = true;

                if(saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    // only correct if face mode is used

                    saveDirectory = saveFileDialog.FileName;//Path.GetFullPath(saveFileDialog.FileName);    

                    /*
                    saveCoordinates();
                    Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, Constants.modeFRectScale);
                    Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer, faceModeSize);
                    Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, Constants.modeFRectScale, true);
                    */

                    save();

                    savedAs = true;
                }

            }
        }

        private void save()
        {
            saveCoordinates();
            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale);
            Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer, faceModeSize);
            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (loaded)
            {
                if (MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    // save logic

                    if (!savedAs)
                        saveAs();
                    else
                    {
                        save();
                        MessageBox.Show(Constants.progressSaved, Constants.progressSavedCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
            }
            
            Application.Exit();
            
        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show(Constants.AboutMe, Constants.Version);
        }

        private void faceDetectionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            faceElementsDetectionToolStripMenuItem.Checked = false;
            faceDetectionToolStripMenuItem.Checked = true;

            if (loaded)
            {
                if (MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    // save logic
                    if (!savedAs)
                        saveAs();
                    else
                        save();
                }

            }

            MessageBox.Show(Constants.modeSwitchInformation, "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

            //if (!modeSet)
            mode = Utilities.switchMode(faceDetectionToolStripMenuItem, faceElementsDetectionToolStripMenuItem);
        }

        private void faceElementsDetectionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            faceDetectionToolStripMenuItem.Checked = false;
            faceElementsDetectionToolStripMenuItem.Checked = true;

            if (loaded)
            {
                if (MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    // save logic
                    if (!savedAs)
                        saveAs();
                    else
                        save();
                }

            }

            MessageBox.Show(Constants.modeSwitchInformation, "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

            //if (!modeSet)
            mode = Utilities.switchMode(faceDetectionToolStripMenuItem, faceElementsDetectionToolStripMenuItem);
        }

        private void exportNormalizedCsvToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if(!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaptionExport, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                if(!savedAs)
                {

                    if (!String.IsNullOrEmpty(csvPath))
                    {
                        saveDirectory = csvPath;
                        save();
                    }
                    else
                    {
                        MessageBox.Show(Constants.pleaseSave, Constants.pleaseSaveCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
                        saveAs();
                    }
                }
                else
                {
                    save();
                }


                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "CSV File|*.csv|All files|*.*";
                saveFileDialog.Title = "Export normalized .csv File";
                saveFileDialog.RestoreDirectory = true;

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    exportDirectory = saveFileDialog.FileName;
                    exportMinMaxDirectory = Path.Combine(Path.GetDirectoryName(saveFileDialog.FileName),
                                            Path.GetFileNameWithoutExtension(saveFileDialog.FileName) + "_min_max.csv");

                    exportNormalized();
                }

            }

        }

        private void exportNormalized()
        {
            Tuple<List<List<double>>, List<List<int>>> normalized;
            Tuple<List<List<double>>, List<List<int>>> normalizedFS;
            CoordinatesContainer<double> normalizedCoordinates;
            CoordinatesContainer<double> normalizedFaceSize;
            CoordinatesContainer<int> minMaxCoord;
            CoordinatesContainer<int> minMaxFS;

            saveCoordinates();

            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale);

            normalized = Utilities.normalizeOutput<double, int>(realCoordinatesList);
            normalizedFS = Utilities.normalizeOutput<double, int>(faceModeSize);

            normalizedCoordinates = new CoordinatesContainer<double>(normalized.Item1);
            minMaxCoord = new CoordinatesContainer<int>(normalized.Item2);
            normalizedFaceSize = new CoordinatesContainer<double>(normalizedFS.Item1);
            minMaxFS = new CoordinatesContainer<int>(normalizedFS.Item2);

            Utilities.writeToCSV(mode, normalizedCoordinates, imageNames, lookAngleContainer, normalizedFaceSize, true);
            Utilities.writeMinMax(mode, minMaxCoord, minMaxFS, "MinMaxValues");

            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);
        }

    }
}
