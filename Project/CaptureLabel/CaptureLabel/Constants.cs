using System;

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
    }
}
