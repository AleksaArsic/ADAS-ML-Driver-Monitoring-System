using System;
using System.Drawing;
using System.Windows.Forms;

namespace CaptureLabel
{
    static class Constants
    {
        // general information
        public static readonly string Version = "CaptureLabel v0.1";
        public static readonly string AboutMe = "Author: Aleksa Arsic \nEmail: arsicaleksa96@gmail.com";

        // supported fromtas
        public static readonly String[] supportedFormats = { ".jpeg", ".jpg", ".png" };

        // image scale minimal and maximal factor
        public static readonly float imageScaleMin = 1.0f;
        public static readonly float imageScaleMax = 2.0f;

        // work information strings
        public static readonly string errorCaption = "Error!";
        public static readonly string pathExceptionMsg = "Path not valid.";
        public static readonly string csvFileNameExceptionMsg = "Input file is not .csv file format";
        public static readonly string pleaseImport = "Please import data first";
        public static readonly string pleaseImportCaption = "Nothing to be saved";
        public static readonly string pleaseImportCaptionExport = "Nothing to be exported";
        public static readonly string pleaseSave = "Please save your progress";
        public static readonly string pleaseSaveCaption = "Please save";
        public static readonly string saveProgressString = "All changes will be deleted. Do you want to save them?";
        public static readonly string progressSaved = "Progress saved successfully";
        public static readonly string progressSavedCaption = "Progress saved";
        public static readonly string modeSwitchInformation = "Please re-import data to complete mode switch.";

        // check box strings
        public static readonly string faceAngleCB = "Face angle";
        public static readonly string lookAngleCB = "Look angle";

        // initial rectangle starting positions
        public static readonly int[] rectStartPos = { 200, 200 };

        // char's denoting selected mode
        public static readonly char faceMode = 'f';
        public static readonly char faceElementsMode = 'e';
        public static readonly char eyeContourMode = 'g';

        // face elements and eye countour mode keyboard shortcuts
        public static readonly Keys[] focusShortcutsE =
        {
            Keys.D1,
            Keys.D2,
            Keys.D3,
            Keys.Q,
            Keys.W
        };

        // face mode keyboard shortcuts
        public static readonly Keys[] focusShortcutsF =
        {
            Keys.D1,
            Keys.D2,
            Keys.D3
        };

        // status bar strings
        public static readonly string imageCounterString = "Image: ";
        public static readonly string inFocusString = "Currently in focus: ";

        // face elements mode rectangle names
        public static readonly string[] rectangleNameE =
        {
            "Left Eye",
            "Right Eye",
            "Nose",
            "Mouth Up",
            "Mouth Down"
        };

        // look angle chekbox strings
        public static readonly string[] lookingAngleString =
            { "Left", "Right", "Up", "Down" };

        // face mode rectangle names
        public static readonly string[] rectangleNameF =
        {
            "Face",
            "Left eye",
            "Right eye "
        };

        // eye countour mode rectangle names
        public static readonly string[] rectangleNameG =
        { 
            "Center Up", 
            "Center", 
            "Center Down", 
            "Left Point", 
            "Right Point" 
        };

        // initial rectangle size
        public static Size rectSize = new Size(10, 10);

        // face mode initial starting positions
        public static readonly int[] faceModeStartPos =
        {
            200, 200,

            250, 250,
            350, 250
        };

        // face elements mode initial starting positions
        public static readonly int[] faceElementStartPos =
        {
            // (x, y)
            300, 225,

            // RIGHT EYE
            700, 225,

            // NOSE
            500, 400,

            // MOUTH
            // mouthUp
            500, 500,
            // mouthDown
            500, 600
        };

        // eye countour mode initial starting positions
        public static readonly int[] eyeContourStartPos =
        {
            // (x, y)

            // center high point
            500, 300,
            // center point
            500, 400,
            // center low point 
            500, 500,
            // left point
            300, 400,
            // right point
            700, 400
        };

        // face mode initial sizes
        public static readonly Size[] faceModeStartSize =
        {
            new Size(200, 300),
            new Size(10, 10),
            new Size(10, 10)
        };

        // change in size for face recctangle in face mode
        public static readonly int modeFRectDeltaSize = 3; // in px
        // constant width to height ration for every rectangle 2:3
        public static readonly double modeFRectScale = 1.5d; // 2:3
    }
}
