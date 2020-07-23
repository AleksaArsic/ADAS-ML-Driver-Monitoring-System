using System;
using System.Windows.Forms;
using System.IO;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Reflection;

namespace CaptureLabel
{

    public partial class CaptureLabel : Form
    {
        // general information fields
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

        // set to true if it's been Saved as in current session
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
        private int[] eyesNotVisible = { 0, 0 };
        private CoordinatesContainer<int> eyesNotVisibleContainer = new CoordinatesContainer<int>();
        private CoordinatesContainer<int> faceModeSize = new CoordinatesContainer<int>();

        private List<int> isFacePresent = new List<int>();
        private List<int> eyeClosed = new List<int>();

        // set to true if past work has been loaded 
        bool loaded = false;

        private char mode = Constants.faceMode;

        private string[] rectangleFocusNames;
        private List<int[]> rectSPostion = new List<int[]>();

        // Constructor
        public CaptureLabel()
        {
            InitializeComponent();
            // double buffering to remove flickering when scrolling trough images
            typeof(Panel).InvokeMember("DoubleBuffered", BindingFlags.SetProperty
               | BindingFlags.Instance | BindingFlags.NonPublic, null,
               imagePanel, new object[] { true });

            // initialize defualt rectangle positions
            start();

            //initializes selected mode
            initMode(mode);
            
        }

        // variables initialized only once, at the beginning
        // initializes default rectangle positions at the beginning of the programm
        private void start()
        {
            rectSPostion.Add(Constants.faceElementStartPos);
            rectSPostion.Add(Constants.faceModeStartPos);
            rectSPostion.Add(Constants.eyeContourStartPos);
        }

        // keyboard event handler
        private void CaptureLabel_KeyDown(object sender, KeyEventArgs e)
        { 
            // scorll up or down depending on key pressed
            if(e.KeyCode == Keys.PageUp || e.KeyCode == Keys.PageDown)
            {
                // save all rectangles coordinates
                saveCoordinates();

                if (e.KeyCode == Keys.PageDown)
                    scrollDown();
                if (e.KeyCode == Keys.PageUp)
                    scrollUp();

                // if there are no values for current image set them to initial position
                if (!isLoaded)
                    rectangles.resetCoordinates(rectSPostion[mode - Constants.faceElementsMode]);

                // reset relevant fields 
                rectangles.resetFocusList();
                someoneIsInFocus = false;
                imagePanel.Refresh();
               
            }

            // paste previous picture rectangles to current picture
            if (e.KeyCode == Keys.X && currentImageIndex >= 1)
            {
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
                }
                if (e.KeyCode == Keys.Right)
                {
                    rectangles.addToFocused(1, 0);
                    imagePanel.Refresh();
                }
                if (e.KeyCode == Keys.Down)
                {
                    rectangles.addToFocused(0, 1);
                    imagePanel.Refresh();
                }
                if (e.KeyCode == Keys.Up)
                {
                    rectangles.addToFocused(0, -1);
                    imagePanel.Refresh();
                }
            }

            // Set focus based on keyboard shortcut
            // for face mode this will cause error. 
            // index out of range when setting focus on elements past index 2 
            // in focusShortcuts array
            Keys[] focusShortcuts = (mode == Constants.faceMode ? Constants.focusShortcutsF : Constants.focusShortcutsE);

            if (Array.Exists(focusShortcuts, 
                            element => element == e.KeyCode) &&
                            !imagePathTB.Focused && !csvPathTB.Focused)
            {
                rectangles.resetFocusList();
                rectangles.setFocus(Array.IndexOf(focusShortcuts, e.KeyCode));
                someoneIsInFocus = true;
                imagePanel.Refresh();
            }

        }

        // mouse event handler 
        private void imagePanel_MouseDown(object sender, MouseEventArgs e)
        {
            // if not on image panel do nothing
            if (!imagePanel.ClientRectangle.Contains(e.Location)) return;
            
            if(e.Button == MouseButtons.Left)
            {
                // set rect in focus
                currentlyInFocus = rectangles.contains(e.Location);
                if (currentlyInFocus.Item1)
                {
                    rectangles.resetFocusList();
                    someoneIsInFocus = true;
                    if(someoneIsInFocus)
                        rectangles.setFocus(currentlyInFocus.Item2);
                    imagePanel.Refresh();
                }
                else
                {
                    int inFocus = rectangles.inFocusIndex();
                    Rectangle rectInFocus = rectangles.findInFocus();

                    // set rectangle center coordinates to mouse coordinates
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

            // change focus when mouse keys are released
            if(someoneIsInFocus)
            {
                someoneIsInFocus = false;
                rectangles.resetFocusList();
                imagePanel.Refresh();
            }
            
        }

        // move rectangles based on mouse movement
        private void imagePanel_MouseMove(object sender, MouseEventArgs e)
        {
            // if the mouse is on the focused rectangle and left mouse key is pressed, move it
            if (e.Button == MouseButtons.Left && someoneIsInFocus)
            {
                Rectangle rectInFocus = rectangles.findInFocus();

                // Increment rectangle-location by mouse-location delta.
                int x = e.X - rectInFocus.X - rectInFocus.Width / 2;
                int y = e.Y - rectInFocus.Y - rectInFocus.Height / 2;

                rectangles.addToFocused(x, y);

                imagePanel.Refresh();
            }         
        }

        // scroll trough images with mouse wheel
        private void imagePanel_MouseWheel(object sender, MouseEventArgs e)
        {
            
            if (!imagePanel.ClientRectangle.Contains(e.Location) || imagePanel.BackgroundImage == null) return;

            // change size of face rectangle in face mode
            if(mode == Constants.faceMode && Control.ModifierKeys == Keys.Control)
            {
                if (e.Delta > 0)
                    rectangles.rescaleRect(0, Constants.modeFRectDeltaSize, Constants.modeFRectScale);
                else
                    rectangles.rescaleRect(0, -Constants.modeFRectDeltaSize, Constants.modeFRectScale);

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
                rectangles.resetCoordinates(rectSPostion[mode - Constants.faceElementsMode]);

            rectangles.resetFocusList();
            someoneIsInFocus = false;
            imagePanel.Refresh();

        }
        
        // update rectangles and every compononent that needs to be redrawn
        private void imagePanel_Paint(object sender, PaintEventArgs e)
        {
            if (!loaded)
                return;

            Rectangle[] rects = rectangles.getRectangles();
            int inFocus = rectangles.inFocusIndex();

            // dont fill face rectangle in face mode with solid color if focused
            for(int i = 0; i < rects.Length; i++)
            {
                if((mode != Constants.faceMode && inFocus == i) || (mode == Constants.faceMode && i != 0 && inFocus == i))
                    e.Graphics.FillRectangle(new SolidBrush(Color.Red), rects[i]);
                else
                    e.Graphics.DrawRectangle(new Pen(Color.Red), rects[i]);
            }

            // change in focus status bar
            if(someoneIsInFocus)
                    inFocusLabel.Text = Constants.inFocusString + " " + rectangleFocusNames[rectangles.inFocusIndex()];

            // change current image index if changed
            imageCounterLabel.Text = Constants.imageCounterString + " " + (currentImageIndex + 1).ToString() + "/" + imageLocation.Count.ToString();

            imagePanel.Focus();
        }

        // set imageFolder to imagePathTB textbox 
        private void imagePathTB_TextChanged(object sender, EventArgs e)
        {
            imageFolder = imagePathTB.Text;
        }

        // set csvPath to csvPathTB textbox 
        private void csvPathTB_TextChanged(object sender, EventArgs e)
        {
            csvPath = csvPathTB.Text;
        }

        // import button logic 
        private void importButton_Click(object sender, EventArgs e)
        {
            Cursor.Current = Cursors.WaitCursor;

            // release everything from memory before new import (or new import)
            cleanUp();

            // initialize selected mode
            initMode(mode);

            try
            {            
                // get list of everything in folder passed to imageFolder
                imageLocation = new List<string>(Directory.GetFiles(imageFolder));
                csvFileName = new DirectoryInfo(imageFolder).Name;

                var sortedFiles = Directory.GetFiles(@"C:\", "*").OrderByDescending(d => new FileInfo(d).CreationTime);

                // Parse list of image locations to contain only image locations
                imageLocation = Utilities.parseImagesToList(imageLocation);

                // import only if there are images found in folder
                if (imageLocation.Count > 0)
                {
                    // set imagePanel to first image
                    imagePanel.BackgroundImage = Image.FromFile(imageLocation[0]);
                    currentImageIndex = 0;

                    // extract image names
                    foreach(string name in imageLocation)
                        imageNames.Add(Path.GetFileNameWithoutExtension(name));

                    // check for existing .csv file
                    if(!String.IsNullOrEmpty(csvPath) && csvPath.Contains(".csv"))
                    {
                        // parse .csv file based on mode selected
                        Tuple<List<int>, List<CoordinatesContainer<int>>> tempCSV = Utilities.parseCSV(csvPath, mode);

                        // set mode relevant fields
                        if (mode == Constants.faceMode)
                            isFacePresent = tempCSV.Item1;
                        if (mode == Constants.faceElementsMode)
                            eyesNotVisibleContainer = new CoordinatesContainer<int>(tempCSV.Item2[3]);
                        if (mode == Constants.eyeContourMode)
                            eyeClosed = tempCSV.Item1;

                        // set relevant fields to ones that are parsed from .csv file
                        realCoordinatesList = new CoordinatesContainer<int>(tempCSV.Item2[0]);
                        lookAngleContainer = new CoordinatesContainer<int>(tempCSV.Item2[1]);
                        faceModeSize = new CoordinatesContainer<int>(tempCSV.Item2[2]);

                        // calculate resize factor between original image and image on the imagePanel
                        for (int i = 0; i < imageNames.Count; i++)
                        {
                            imagePanel.BackgroundImage = Image.FromFile(imageLocation[i]);
                            calculateResizeFactor(i);
                            imagePanel.BackgroundImage.Dispose();
                        }

                        // correct face coordinates
                        if (mode == Constants.faceMode)
                            Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);

                        List<int> singleRow;
                        // set rectangle coordinates based on real one read from .csv file
                        for (int i = 0; i < realCoordinatesList.getSize(); i++)
                        {
                            singleRow = realCoordinatesList.getRow(i);
                            coordinatesList.addRow(new List<int>(calculateRectangleCoordinates(singleRow, i)));
                        }

                        // load currentImageIndex image from file and load associated coordinates
                        imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                        loadCoordinates(currentImageIndex);

                    }
                    imagePathTB.ReadOnly = true;
                    loaded = true;
                }
            }
            // catch if something went wrong in the section above
            catch (Exception msg)
            {
                imagePathTB.ReadOnly = false;
                MessageBox.Show(msg.Message, Constants.errorCaption, MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            imagePanel.Refresh();

            Cursor.Current = Cursors.Default;
        }

        // scroll down trough images
        private void scrollDown()
        {
            currentImageIndex++;

            // load new image if there is one to load
            if (currentImageIndex < imageLocation.Count)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                isLoaded = loadCoordinates(currentImageIndex);
            }
            else
            {
                currentImageIndex = imageLocation.Count - 1;
            }
        }

        // scroll up trough images
        private void scrollUp()
        {
            currentImageIndex--;

            // load new image if there is one to load
            if (currentImageIndex < 0)
                currentImageIndex = 0;

            if (imageLocation.Count > 0)
            {
                imagePanel.BackgroundImage.Dispose();
                imagePanel.BackgroundImage = Image.FromFile(imageLocation[currentImageIndex]);
                isLoaded = loadCoordinates(currentImageIndex);
            }
        }

        // save coordinates of the current image index
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

            int faceWidth = (mode == Constants.faceMode) ? rectangles.getRectangles()[0].Width : imagePanel.BackgroundImage.Width;
            
            // calculate real coordinates
            if (coordinatesList.getRow(currentImageIndex) == null)
            {
                // add new properties associated with this image, some are based on current mode
                lookAngleContainer.addRow(lookAngle.ToList());
                faceModeSize.addRow(new List<int> { faceWidth });
                coordinatesList.addRow(coordinates);
                realCoordinatesList.addRow(calculateRealCoordinates(coordinates));

                if (mode == Constants.faceMode)
                    isFacePresent.Add((noFaceCB.Checked ? 1 : 0));
                if (mode == Constants.faceElementsMode)
                    eyesNotVisibleContainer.addRow(eyesNotVisible.ToList());
                if (mode == Constants.eyeContourMode)
                    eyeClosed.Add((eyeClosedCB.Checked ? 1 : 0));
            }
            else
            {
                // replace new properties associated with this image, some are based on current mode
                lookAngleContainer.replaceRow(lookAngle.ToList(), currentImageIndex);
                coordinatesList.replaceRow(coordinates, currentImageIndex);
                realCoordinatesList.replaceRow(calculateRealCoordinates(coordinates), currentImageIndex);
                faceModeSize.replaceRow(new List<int> { faceWidth }, currentImageIndex);

                if (mode == Constants.faceMode)
                    isFacePresent[currentImageIndex] = (noFaceCB.Checked ? 1 : 0);
                if (mode == Constants.faceElementsMode)
                    eyesNotVisibleContainer.replaceRow(eyesNotVisible.ToList(), currentImageIndex);
                if (mode == Constants.eyeContourMode)
                    eyeClosed[currentImageIndex] = (eyeClosedCB.Checked ? 1 : 0);
            }

            // set look angle and checkbox states
            lookAngle = new int[] { 0, 0, 0, 0 };
            setCheckBoxes(new CheckBox[] { leftCB, rightCB, upCB, downCB });

            if (mode == Constants.faceElementsMode)
            {
                eyesNotVisible = new int[] { 0, 0 };
                setEyesCheckBoxes(new CheckBox[] { LEnotVCB, REnotVCB });
            }
            if (mode == Constants.faceMode)
                noFaceCB.Checked = false;
            if (mode == Constants.eyeContourMode)
                eyeClosedCB.Checked = false;
        }

        // load coordinates of the current image index
        private bool loadCoordinates(int index)
        {
            // if there are no coordinates to load, return
            if (index >= realCoordinatesList.getSize())
                return false;

            // get corresponding coordinates and checkbox states
            List<int> singleRow = coordinatesList.getRow(index);
            List<int> faceSize = faceModeSize.getRow(index);
            lookAngle = new int[] { 0, 0, 0, 0 };
            eyesNotVisible = new int[] { 0, 0 };

            if(mode == Constants.faceMode)
                noFaceCB.Checked = (isFacePresent[index] == 0 ? false : true);
            if (mode == Constants.eyeContourMode)
                eyeClosedCB.Checked = (eyeClosed[index] == 0 ? false : true);

            // set rectangle positions and checkbox states based on retireved values
            if (singleRow != null)
            {
                rectangles.setAllRectCoordinates(singleRow);
                lookAngle = lookAngleContainer.getRow(index).ToArray();

                if (mode == Constants.faceElementsMode)
                {
                    eyesNotVisible = eyesNotVisibleContainer.getRow(index).ToArray();
                    setEyesCheckBoxes(new CheckBox[] { LEnotVCB, REnotVCB });
                }

                if (mode == Constants.faceMode)
                {
                    rectangles.setRectSize(0, new Size(faceSize[0], (int)(faceSize[0] * Constants.modeFRectScale)));
                }

                setCheckBoxes(new CheckBox[] { leftCB, rightCB, upCB, downCB });
                return true;
            }
            
            
            return false;
        }

        // calculate resize factor between original image and image on the imagePanel
        private void calculateResizeFactor(int index)
        {
            if (imagePanel.BackgroundImage == null)
                return;

            int realW = imagePanel.BackgroundImage.Width;
            int realH = imagePanel.BackgroundImage.Height;
            int currentW = imagePanel.Width;
            int currentH = imagePanel.Height;

            // calculate resize factors
            double wFactor = (double)currentW / realW;
            double hFactor = (double)currentH / realH;

            // use minimal from two of the above
            double resizeFactor = Math.Min(wFactor, hFactor);

            // calculate padding to be added
            // this is done to presereve aspect ratio
            double padX = resizeFactor == wFactor ? 0 : (currentW - (resizeFactor * realW)) / 2;
            double padY = resizeFactor == hFactor ? 0 : (currentH - (resizeFactor * realH)) / 2;

            // assigne resize factor the corresponding image
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

        // calculate rectangle coordinates on the original image
        private List<int> calculateRealCoordinates(List<int> l)
        {

            List<int> realCoordinates = new List<int>();

            int tempX = 0;
            int tempY = 0;

            // loop trough relative coordinates and calculate corresponding X and Y coordinates on the original image
            for (int i = 0; i < l.Count; i += 2)
            {
                tempX = (int)(Math.Round((l[i] - imagePadX[currentImageIndex]) / imageResizeFactor[currentImageIndex], MidpointRounding.AwayFromZero));
                tempY = (int)(Math.Round((l[i + 1] - imagePadY[currentImageIndex]) / imageResizeFactor[currentImageIndex], MidpointRounding.AwayFromZero));
                realCoordinates.Add(tempX);
                realCoordinates.Add(tempY);
            }

            return realCoordinates;
        }

        // calculate rectangle coordinates on the imageView panel image
        private List<int> calculateRectangleCoordinates(List<int> l, int index)
        {
            List<int> rectCoordinates = new List<int>();

            int tempX = 0;
            int tempY = 0;

            // loop trough real coordinates of the original image 
            // and calculate corresponding X and Y coordinates on the imageView panel image
            for (int i = 0; i < l.Count; i += 2)
            {
                tempX = (int)(Math.Round((l[i] * imageResizeFactor[index]), MidpointRounding.AwayFromZero) + imagePadX[index]);
                tempY = (int)(Math.Round((l[i + 1] * imageResizeFactor[index]), MidpointRounding.AwayFromZero) + imagePadY[index]);
                rectCoordinates.Add(tempX);
                rectCoordinates.Add(tempY);
            }

            return rectCoordinates;
        }

        // clean up function 
        // called when importing or re-importing data and when New is selected from the File menu
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
            eyesNotVisibleContainer = null;
            isFacePresent = null;
            eyeClosed = null;

            currentImageIndex = 0;
            isLoaded = false;
            someoneIsInFocus = false;
            savedAs = false;

            imageLocation = new List<string>();
            imageNames = new List<string>();
            imageResizeFactor = new List<double>();
            imagePadX = new List<double>();
            imagePadY = new List<double>();
            coordinatesList = new CoordinatesContainer<int>();
            realCoordinatesList = new CoordinatesContainer<int>();

            faceModeSize = new CoordinatesContainer<int>();
            lookAngleContainer = new CoordinatesContainer<int>();
            eyesNotVisibleContainer = new CoordinatesContainer<int>();
            isFacePresent = new List<int>();
            eyeClosed = new List<int>();
    }

    // initialize selected mode
    private void initMode(char currentMode)
        {
            // initialize face mode and show appropriate group box properties
            if (currentMode == Constants.faceMode)
            {
                rectangles = new RectangleContainer(3, Constants.faceModeStartPos, Constants.faceModeStartSize);
                lookAngleGB.Text = Constants.faceAngleCB;
                faceOptionsGB.Visible = true;
                eyePropertiesGB.Visible = false;
                eyePropertiesCGB.Visible = false;

                rectangleFocusNames = Constants.rectangleNameF;
            }

            // initialize face elements mode and show appropriate group box properties
            if (currentMode == Constants.faceElementsMode)
            {
                rectangles = new RectangleContainer(5, Constants.faceElementStartPos, Constants.rectSize);
                lookAngleGB.Text = Constants.lookAngleCB;
                faceOptionsGB.Visible = false;
                eyePropertiesGB.Visible = true;
                eyePropertiesCGB.Visible = false;

                rectangleFocusNames = Constants.rectangleNameE;

            }

            // initialize eye countour mode and show appropriate group box properties
            if (currentMode == Constants.eyeContourMode)
            {
                rectangles = new RectangleContainer(5, Constants.eyeContourStartPos, Constants.rectSize);
                lookAngleGB.Text = Constants.lookAngleCB;
                faceOptionsGB.Visible = false;
                eyePropertiesGB.Visible = false;
                eyePropertiesCGB.Visible = true;

                rectangleFocusNames = Constants.rectangleNameG;
            }
        }

        // change leftCB state
        private void leftCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(leftCB, 0);
            rightCB.Checked = false;
        }

        // change rightCB state
        private void rightCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(rightCB, 1);
            leftCB.Checked = false;
        }

        // change upCB state
        private void upCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(upCB, 2);
            downCB.Checked = false;
        }

        // change downCB state
        private void downCB_CheckedChanged(object sender, EventArgs e)
        {
            setLookAngle(downCB, 3);
            upCB.Checked = false;
        }

        // set look angle checkboxes
        private void setLookAngle(CheckBox cb, int index)
        {
            lookAngle[index] = cb.Checked ? 1 : 0;
        }

        // change states of look angle checkboxes
        private void setCheckBoxes(CheckBox[] lookAngleCBs)
        {
            for(int i = 0; i < lookAngleCBs.Length; i++)
            {
                lookAngleCBs[i].Checked = (lookAngle[i] == 1 ? true : false);
            }
        }

        // called when selected from File -> New 
        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // ask user if he wishes to save his progress because it will be lost
            if(MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
            {
                // save logic
                if (!savedAs)
                    saveAs();
                else
                    save();
            }
            
            // set program into initial state
            loaded = false;
            imagePanel.BackgroundImage = null;
            imagePathTB.Text = "";
            csvPathTB.Text = "";
            cleanUp();
            imagePanel.Refresh();
            
        }

        // called when selected from File -> Save
        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // check if there is any work to be saved
            if (!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                // save logic
                if(!savedAs)
                    saveAs();
                else
                    save();
            }
        }

        // called when selected from File -> Save as 
        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // save as logic
            saveAs();
        }

        // Save as logic called when selected from File -> Save as
        private void saveAs()
        {
            // check if there is any work to be saved
            if (!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaption, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                // open Save file dialog and get relevant fields
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "CSV File|*.csv|All files|*.*";
                saveFileDialog.Title = "Save .csv File";
                saveFileDialog.RestoreDirectory = true;

                // save logic
                if(saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    saveDirectory = saveFileDialog.FileName;   

                    save();

                    savedAs = true;
                }

            }
        }

        // called when selected from File -> Save
        private void save()
        {
            // save current image index coordinates
            saveCoordinates();

            // check which mode is selected and save appropriately 
            // face mode save logic
            if (mode == Constants.faceMode)
            {
                // correct face coordinates and write them to .csv file
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale);
                Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer, faceModeSize, elementState: isFacePresent);
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);
            }
            // face elements mode save logic
            if (mode == Constants.faceElementsMode)
                Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer, 
                    faceModeSize, eyesNotVisibleContainer : eyesNotVisibleContainer);
            // eye countour mode save logic
            if (mode == Constants.eyeContourMode)
                Utilities.writeToCSV(mode, realCoordinatesList, imageNames, lookAngleContainer,
                    faceModeSize, elementState : eyeClosed);
        }

        // called when selected from File -> Exit
        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // if there is work in progress ask use if he wishes to save it because it will be lost
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
            
            // exit from application
            Application.Exit();
            
        }

        // called when selected from Other -> about
        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show(Constants.AboutMe, Constants.Version);
        }

        // called when selected from Mode -> Face mode
        private void faceDetectionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // set information about which mode is selected
            faceElementsDetectionToolStripMenuItem.Checked = false;
            eyeContourDetectionToolStripMenuItem.Checked = false;
            faceDetectionToolStripMenuItem.Checked = true;

            // if there is work in progress ask use if he wishes to save it because it will be lost
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

                MessageBox.Show(Constants.modeSwitchInformation, "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            // switch mode
            mode = Utilities.switchMode(new ToolStripMenuItem[] { faceDetectionToolStripMenuItem, faceElementsDetectionToolStripMenuItem, eyeContourDetectionToolStripMenuItem });
        }

        // called when selected from Mode -> Face elements mode
        private void faceElementsDetectionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // set information about which mode is selected
            faceDetectionToolStripMenuItem.Checked = false;
            eyeContourDetectionToolStripMenuItem.Checked = false;
            faceElementsDetectionToolStripMenuItem.Checked = true;

            // if there is work in progress ask use if he wishes to save it because it will be lost
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

                MessageBox.Show(Constants.modeSwitchInformation, "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            // switch mode
            mode = Utilities.switchMode(new ToolStripMenuItem[] { faceDetectionToolStripMenuItem, faceElementsDetectionToolStripMenuItem, eyeContourDetectionToolStripMenuItem });
        }

        // called when selected from Mode -> Eye countour mode
        private void eyeContourDetectionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // set information about which mode is selected
            faceElementsDetectionToolStripMenuItem.Checked = false;
            faceDetectionToolStripMenuItem.Checked = false;
            eyeContourDetectionToolStripMenuItem.Checked = true;

            // if there is work in progress ask use if he wishes to save it because it will be lost
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

                MessageBox.Show(Constants.modeSwitchInformation, "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            // switch mode
            mode = Utilities.switchMode(new ToolStripMenuItem[] { faceDetectionToolStripMenuItem, faceElementsDetectionToolStripMenuItem, eyeContourDetectionToolStripMenuItem });

        }

        // called when selected from File -> Export normalized .csv
        private void exportNormalizedCsvToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // check if there is any work to be exported
            if(!loaded)
            {
                MessageBox.Show(Constants.pleaseImport, Constants.pleaseImportCaptionExport, MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                // if the work is not save ask user to first save it to normal .csv file
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

                // open save file dialog and set relevant fields
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "CSV File|*.csv|All files|*.*";
                saveFileDialog.Title = "Export normalized .csv File";
                saveFileDialog.RestoreDirectory = true;

                // export values to normalized .csv file
                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    exportDirectory = saveFileDialog.FileName;
                    exportMinMaxDirectory = Path.Combine(Path.GetDirectoryName(saveFileDialog.FileName),
                                            Path.GetFileNameWithoutExtension(saveFileDialog.FileName) + "_min_max.csv");
                    // export normalized values
                    exportNormalized();
                }

            }

        }

        // exports values to normalized .csv file based on current work mode
        private void exportNormalized()
        {
            Tuple<List<List<double>>, List<List<int>>> normalized;
            Tuple<List<List<double>>, List<List<int>>> normalizedFS;
            CoordinatesContainer<double> normalizedCoordinates;
            CoordinatesContainer<double> normalizedFaceSize;
            CoordinatesContainer<int> minMaxCoord;
            CoordinatesContainer<int> minMaxFS;

            // save current image index values
            saveCoordinates();

            // export logic for face mode 
            if (mode == Constants.faceMode)
            {
                // correct face coordinates
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale);

                // normalize coordinates and face size values
                normalized = Utilities.normalizeOutput<double, int>(realCoordinatesList);
                normalizedFS = Utilities.normalizeOutput<double, int>(faceModeSize);

                // asing values to appropriate value containers
                normalizedCoordinates = new CoordinatesContainer<double>(normalized.Item1);
                minMaxCoord = new CoordinatesContainer<int>(normalized.Item2);
                normalizedFaceSize = new CoordinatesContainer<double>(normalizedFS.Item1);
                minMaxFS = new CoordinatesContainer<int>(normalizedFS.Item2);

                // write normalized coordinates .csv file
                Utilities.writeToCSV(mode, normalizedCoordinates, imageNames, lookAngleContainer, normalizedFaceSize,
                                     isFacePresent, normalized: true);

                // create .csv file with minimal and maximal values needed for denormalization 
                Utilities.writeMinMax(mode, minMaxCoord, minMaxFS);

                // correct face coordinates
                Utilities.correctFaceCoordinates(realCoordinatesList, faceModeSize, imageResizeFactor, Constants.modeFRectScale, true);
            }
            // export logic for face elements mode and eye countour mode
            else
            {
                // normalize coordinates and face size values
                normalized = Utilities.normalizeOutput<double, int>(realCoordinatesList, faceModeSize, Constants.faceElementsMode);
                normalizedFS = Utilities.normalizeOutput<double, int>(faceModeSize);

                // asing values to appropriate value containers
                normalizedCoordinates = new CoordinatesContainer<double>(normalized.Item1);
                minMaxCoord = new CoordinatesContainer<int>(normalized.Item2);
                normalizedFaceSize = new CoordinatesContainer<double>(normalizedFS.Item1);
                minMaxFS = new CoordinatesContainer<int>(normalizedFS.Item2);

                // write normalized coordinates .csv file
                Utilities.writeToCSV(mode, normalizedCoordinates, imageNames, lookAngleContainer,
                    faceModeSize, eyesNotVisibleContainer: eyesNotVisibleContainer, elementState: eyeClosed, normalized: true);
                // create .csv file with minimal and maximal values needed for denormalization 
                Utilities.writeMinMax(mode, minMaxCoord, minMaxFS);

            }
        }

        // change state of LEnotVCB
        private void LEnotVCB_CheckedChanged(object sender, EventArgs e)
        {
            REnotVCB.Checked = false;
            setEyesNotVisible(LEnotVCB, 0);

        }

        // change state of REnotVCB
        private void REnotVCB_CheckedChanged(object sender, EventArgs e)
        {
            LEnotVCB.Checked = false;
            setEyesNotVisible(REnotVCB, 1);

        }

        // change state of eyes not visible checkboxes
        private void setEyesNotVisible(CheckBox cb, int index)
        {
            eyesNotVisible[index] = cb.Checked ? 1 : 0;
        }

        // change state of eyes not visible checkboxes
        private void setEyesCheckBoxes(CheckBox[] eyesNotVisibleCBs)
        {
            for (int i = 0; i < eyesNotVisibleCBs.Length; i++)
            {
                eyesNotVisibleCBs[i].Checked = (eyesNotVisible[i] == 1 ? true : false);
            }
        }

        // called when application is going to be closed
        private void CaptureLabel_FormClosing(Object sender, FormClosingEventArgs e)
        {
            // check if any work is in progress
            if (loaded)
            {
                // ask user to save work in progress because it will be lost.
                if (MessageBox.Show(Constants.saveProgressString, "Caution!", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                {
                    // save logic
                    if (!savedAs)
                        saveAs();
                    else
                        save();
                }
            }
        }
    }
}
