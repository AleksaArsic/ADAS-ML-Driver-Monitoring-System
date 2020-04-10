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

        public static char switchMode(ToolStripMenuItem tsmiFace, ToolStripMenuItem tsmiElements)
        {
            if (tsmiFace.Checked)
                return 'f';
            if (tsmiElements.Checked)
                return 'e';

            return '0';
        }

        public static void writeToCSV<T, U>(char mode, CoordinatesContainer<T> realCoordinatesList, List<string> imageNames, CoordinatesContainer<U> lookAngleContainer, CoordinatesContainer<T> faceModeSize, bool normalized = false)
        {
            bool boolMode = (mode == 'f' ? true : false);
            string csvPath = Path.Combine(new string[] { CaptureLabel.imageFolder, 
                                                        (boolMode ? "FaceMode" : "FaceElement") + 
                                                        CaptureLabel.csvFileName  +
                                                        (normalized ? "_normalized" : "") }) + ".csv";
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

                csv.WriteField("Face width:");
            }

            csv.NextRecord();

            csv.WriteField("Picture:");

            for (int i = 0; i < rectNames.Length; i++)
            {
                csv.WriteField("(x,");
                csv.WriteField("y)");
            }

            csv.NextRecord();

            for (int i = 0; i < realCoordinatesList.getSize(); i++)
            {
                csv.WriteField(imageNames[i]);

                foreach (T value in realCoordinatesList.getRow(i))
                    csv.WriteField(value);

                if (mode == 'f')
                {
                    foreach (U value in lookAngleContainer.getRow(i))
                        csv.WriteField(value);

                    csv.WriteField(faceModeSize.getRow(i)[0]);
                }

                csv.NextRecord();
            }

            writer.Close();
        }

        public static void writeMinMax<T, U>(char mode, CoordinatesContainer<T> minMax, CoordinatesContainer<U> faceModeMinMax, string fileName)
        {
            bool boolMode = (mode == 'f' ? true : false);
            string csvPath = Path.Combine(new string[] { CaptureLabel.imageFolder,
                                                        (boolMode ? "FaceMode" : "FaceElement") +
                                                        fileName }) + ".csv";
            TextWriter writer = new StreamWriter(@csvPath, false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            List<List<T>> minMaxT = new List<List<T>>(minMax.getCoordinates());
            minMaxT = Enumerable.Range(0, minMaxT[0].Count)
                        .Select(i => minMaxT.Select(lst => lst[i]).ToList()).ToList();

            csv.WriteField("");

            string[] rectNames = (boolMode) ? Constants.namesF : Constants.namesE;

            
            foreach (string s in rectNames)
            {
                csv.WriteField(s);
                csv.WriteField("");
            }

            if (boolMode)
                csv.WriteField("Face width:");

            csv.NextRecord();
            csv.WriteField("");

            for (int i = 0; i < rectNames.Length; i++)
            {
                csv.WriteField("(x,");
                csv.WriteField("y)");
            }

            csv.NextRecord();
            csv.WriteField("Min:");

            for (int i = 0; i < minMaxT.Count; i++)
            {

                for(int j = 0; j < minMaxT[i].Count; j++)
                    csv.WriteField(minMaxT[i][j]);

                if(mode == 'f')
                    csv.WriteField(faceModeMinMax.getRow(0)[i]);

                csv.NextRecord();
                csv.WriteField("Max:");
            }

            writer.Close();
        }

        public static CoordinatesContainer<T> readFromCSV<T>(string path, char mode)
        {

            CoordinatesContainer<T> result = new CoordinatesContainer<T>();
            List<T> singleRow = new List<T>();
            T value;
            using (TextReader fileReader = File.OpenText(path))
            {
                var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                csv.Configuration.HasHeaderRecord = false;

                csv.Read();
                csv.Read();

                while (csv.Read())
                {
                    for (int i = 1; csv.TryGetField<T>(i, out value); i++)
                    {
                        if (mode == 'f' && i == 7) break;

                        singleRow.Add(value);
                    }
                    List<T> temp = new List<T>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }

        public static CoordinatesContainer<T> readLookAngleFromCSV<T>(string path)
        {

            CoordinatesContainer<T> result = new CoordinatesContainer<T>();
            List<T> singleRow = new List<T>();
            T value;
            using (TextReader fileReader = File.OpenText(path))
            {
                var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                csv.Configuration.HasHeaderRecord = false;

                csv.Read();
                csv.Read();

                while (csv.Read())
                {
                    for (int i = 7; csv.TryGetField<T>(i, out value); i++)
                    {
                        singleRow.Add(value);
                    }
                    List<T> temp = new List<T>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }

        public static CoordinatesContainer<T> readFaceSizeFromCSV<T>(string path)
        {

            CoordinatesContainer<T> result = new CoordinatesContainer<T>();
            List<T> singleRow = new List<T>();
            T value;
            using (TextReader fileReader = File.OpenText(path))
            {
                var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                csv.Configuration.HasHeaderRecord = false;

                csv.Read();
                csv.Read();

                while (csv.Read())
                {
                    for (int i = 11; csv.TryGetField<T>(i, out value); i++)
                    {
                        singleRow.Add(value);
                    }
                    List<T> temp = new List<T>(singleRow);
                    result.addRow(temp);
                    singleRow.Clear();
                }

            }
            return result;
        }

        public static Tuple<List<List<T>>, List<List<int>>>  normalizeOutput<T, U>(CoordinatesContainer<U> realCoordinatesList)
        {
            CoordinatesContainer<U> retCoordinates = realCoordinatesList;

            List<List<U>> coordinates = new List<List<U>>(realCoordinatesList.getCoordinates());
            List<List<int>> minMaxValues = new List<List<int>>();
            List<List<T>> result = new List<List<T>>();


            // transpose elements
            coordinates = Enumerable.Range(0, coordinates[0].Count)
                        .Select(i => coordinates.Select(lst => lst[i]).ToList()).ToList();

            // normalize elements
            foreach(List<U> l in coordinates)
            {
                int min = Convert.ToInt32(l.Min());
                int max = Convert.ToInt32(l.Max());

                minMaxValues.Add(new List<int>() { min, max });

                List<T> temp = new List<T>();

                for(int i = 0; i < l.Count; i++)
                {
                    double val = (double)(Convert.ToInt32(l[i]) - min) / (max - min);

                    if (Double.IsNaN(val))
                        val = 0;

                    temp.Add((T)(object)val);
                }

                result.Add(temp);
            }

            // transpose elements
            result = Enumerable.Range(0, result[0].Count)
                        .Select(i => result.Select(lst => lst[i]).ToList()).ToList();
            

            return Tuple.Create(result, minMaxValues);
        }
        public static void correctFaceCoordinates(CoordinatesContainer<int> realCoordinatesList, CoordinatesContainer<int> faceModeSize, int scale, bool reverse = false)
        {
            int i = 0;
            // correction factor for the first if face mode
            foreach (List<int> l in realCoordinatesList.getCoordinates())
            {
                int halfWidth = (reverse == false ? faceModeSize.getRow(i)[0] / 2 : -faceModeSize.getRow(i)[0] / 2);
                l[0] = l[0] + halfWidth;
                l[1] = l[1] + halfWidth * scale;
                i++;
            }
        }
    }
}
