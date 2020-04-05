using System;
using System.Windows.Forms;

namespace CaptureLabel
{
    static class Constants
    {
        public static readonly String[] supportedFormats = { ".jpeg", ".jpg", ".png" };
        public static readonly int[] pictureBoxSize = { 968, 764 }; // width, height

        public static readonly float imageScaleMin = 1.0f;
        public static readonly float imageScaleMax = 2.0f;

        public static readonly string errorCaption = "Error!";
        public static readonly string pathExceptionMsg = "Path not valid.";

        public static readonly int[] rectStartPos = { 200, 200 };

        public static readonly Keys[] focusShortcuts = 
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

    }
}
