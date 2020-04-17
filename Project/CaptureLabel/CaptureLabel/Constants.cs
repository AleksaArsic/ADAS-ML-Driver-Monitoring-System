using System;
using System.Drawing;
using System.Windows.Forms;

namespace CaptureLabel
{
    static class Constants
    {
        public static readonly string Version = "CaptureLabel v0.1";
        public static readonly string AboutMe = "Author: Aleksa Arsic \nEmail: arsicaleksa96@gmail.com";

        public static readonly String[] supportedFormats = { ".jpeg", ".jpg", ".png" };

        public static readonly float imageScaleMin = 1.0f;
        public static readonly float imageScaleMax = 2.0f;

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


        public static readonly int[] rectStartPos = { 200, 200 };

        public static readonly Keys[] focusShortcutsE = 
            { 
                Keys.D1,
                Keys.D2,
                Keys.D3,
                Keys.D4,
                Keys.Q,
                Keys.W,
                Keys.E,
                Keys.R,
                Keys.A,
                Keys.S,
                Keys.D
            };

        public static readonly Keys[] focusShortcutsF =
            {
                Keys.D1,
                Keys.D2,
                Keys.D3
            };

        public static readonly string inFocusString = "Currently in focus: ";

        public static readonly string[] rectangleNameE =
        {
            "Left eye Up",
            "Left eye Down",
            "Left eye Left",
            "Left eye Right",
            "Right eye Up",
            "Right eye Down",
            "Right eye Left",
            "Right eye Right",
            "Nose",
            "Mouth Up",
            "Mouth Down"
        };

        public static readonly string[] namesE =
            {"LE Up", "LE Down", "LE Left", "LE Right", "RE Up", "RE Down", "RE Left", "RE Right",
               "Nose", "Mouth Up", "Mouth Down"};

        public static readonly string[] namesF =
            {"Face", "Left eye", "Right eye"};

        public static readonly string[] lookingAngleString =
            {"Left", "Right", "Up", "Down"};

        public static readonly string[] rectangleNameF =
        {
            "Face",
            "Left eye",
            "Right eye "
        };

        public static Size rectSize = new Size(10, 10);

        public static readonly int[] faceElementStartPos =
            {
                // (x, y)

                // LEFT EYE
                // leftEyeUp
                250, 200,
                // leftEyeDown
                250, 250,
                // leftEyeLeft
                200, 225,
                // leftEyeRight
                300, 225,

                // RIGHT EYE
                // rightEyeUp
                750, 200,
                // rightEyeDown
                750, 250,
                // rightEyeLeft
                700, 225,
                // rightEyeRight
                800, 225,

                // NOSE
                500, 400,

                // MOUTH
                // mouthUp
                500, 500,
                // mouthDown
                500, 600
            };

        public static readonly int[] faceModeStartPos =
        {
            200, 200,

            250, 250,
            350, 250
        };

        public static readonly Size[] faceModeStartSize =
        {
            new Size(200, 300),
            new Size(10, 10),
            new Size(10, 10)
        };

        public static readonly int modeFRectDeltaSize = 3; // in px
        public static readonly double modeFRectScale = 1.5d; // 1 : 2
    }
}
