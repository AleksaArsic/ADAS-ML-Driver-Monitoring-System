using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using CsvHelper;

namespace CaptureLabel
{
    static class Utilities
    {
        public static List<string> parseImagesToList(List<string> inList)
        {
            List<string> outList = new List<string>();

            foreach (string item in inList)
            {
                for (int i = 0; i < Constants.supportedFormats.Length; i++)
                {
                    if (item.Contains(Constants.supportedFormats[i]))
                    {
                        outList.Add(item);
                        break;
                    }
                }
            }

            return outList;
        }

        public static Bitmap CaptureScreenShot()
        {
            // get the bounding area of the screen containing (0,0)
            // remember in a multidisplay environment you don't know which display holds this point
            Rectangle bounds = Screen.GetBounds(Point.Empty);

            // create the bitmap to copy the screen shot to
            Bitmap bitmap = new Bitmap(bounds.Width, bounds.Height);

            // now copy the screen image to the graphics device from the bitmap
            using (Graphics gr = Graphics.FromImage(bitmap))
            {
                gr.CopyFromScreen(Point.Empty, Point.Empty, bounds.Size);
            }

            return bitmap;
        }

        public static char switchMode(CheckBox cbFace, CheckBox cbElements)
        {
            if (cbFace.Checked)
                return 'f';
            if (cbElements.Checked)
                return 'e';

            return '0';
        }

        public static void writeToCSV(char mode, RectangleContainer rectangles, CoordinatesContainer realCoordinatesList, List<string> imageNames, CoordinatesContainer lookAngleContainer, CoordinatesContainer faceModeSize)
        {
            bool boolMode = (mode == 'f' ? true : false);
            string csvPath = Path.Combine(new string[] { CaptureLabel.imageFolder, (boolMode ? "FaceMode" : "FaceElement") + CaptureLabel.csvFileName }) + ".csv";
            TextWriter writer = new StreamWriter(@csvPath, false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            csv.WriteField("");

            string[] rectNames = (boolMode) ? Constants.namesF : Constants.namesE;

            foreach (string s in rectNames)
            {
                csv.WriteField(s);
                csv.WriteField("");
            }

            if (boolMode)
            {
                foreach (string s in Constants.lookingAngleString)
                    csv.WriteField(s);

                csv.WriteField("Face size:");
            }

            csv.NextRecord();

            csv.WriteField("Picture:");

            for (int i = 0; i < rectangles.getSize(); i++)
            {
                csv.WriteField("(x,");
                csv.WriteField("y)");
            }

            csv.NextRecord();

            for (int i = 0; i < realCoordinatesList.getSize(); i++)
            {
                csv.WriteField(imageNames[i]);

                foreach (int value in realCoordinatesList.getRow(i))
                    csv.WriteField(value);

                if (mode == 'f')
                {
                    foreach (int value in lookAngleContainer.getRow(i))
                        csv.WriteField(value);

                    csv.WriteField(faceModeSize.getRow(i)[0]);
                }

                csv.NextRecord();
            }

            writer.Close();
        }

        public static CoordinatesContainer readFromCSV(string path, char mode)
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
                        if (mode == 'f' && i == 7) break;

                        singleRow.Add(value);
                    }
                    List<int> temp = new List<int>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }

        public static CoordinatesContainer readLookAngleFromCSV(string path)
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
                    for (int i = 7; csv.TryGetField<int>(i, out value); i++)
                    {
                        singleRow.Add(value);
                    }
                    List<int> temp = new List<int>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }

        public static CoordinatesContainer readFaceSizeFromCSV(string path)
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
                    for (int i = 11; csv.TryGetField<int>(i, out value); i++)
                    {
                        singleRow.Add(value);
                    }
                    List<int> temp = new List<int>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }
    }
}
