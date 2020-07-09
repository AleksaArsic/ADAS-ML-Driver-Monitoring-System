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

        //public static char switchMode(ToolStripMenuItem tsmiFace, ToolStripMenuItem tsmiElements)
        public static char switchMode(ToolStripMenuItem[] tsmi)
        {
            if (tsmi[0].Checked)
                return Constants.faceMode;
            if (tsmi[1].Checked)
                return Constants.faceElementsMode;
            if (tsmi[2].Checked)
                return Constants.eyeContourMode;

            return '0';
        }

        public static void writeToCSV<T, U, X>(char mode, CoordinatesContainer<T> realCoordinatesList, List<string> imageNames, 
                                                CoordinatesContainer<U> lookAngleContainer, CoordinatesContainer<X> faceModeSize, 
                                                List<int> elementState = null, CoordinatesContainer<U> eyesNotVisibleContainer = null, bool normalized = false)
        {
            //bool boolMode = (mode == Constants.faceMode ? true : false);
            // should be embedded in try-catch
            string csvPath = (normalized == true ? CaptureLabel.exportDirectory : CaptureLabel.saveDirectory);
            TextWriter writer = new StreamWriter(@csvPath, false, Encoding.UTF8);
            //TextWriter writer = new StreamWriter(@"D:\Diplomski\DriverMonitoringSystem\Dataset\new.csv", false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            csv.WriteField("");

            string[] rectNames = ((mode == Constants.faceMode) ? Constants.rectangleNameF : (mode == Constants.faceElementsMode ? Constants.rectangleNameE : Constants.rectangleNameG));

            if (mode == Constants.faceMode)
                csv.WriteField("noFace");
            if (mode == Constants.faceElementsMode)
            {
                csv.WriteField("noLeftEye");
                csv.WriteField("noRightEye");
            }
            if (mode == Constants.eyeContourMode)
                csv.WriteField("eyeClosed");

            foreach (string s in rectNames)
            {
                csv.WriteField(s);
                csv.WriteField("");
            }

            //if (boolMode)
            //{
                foreach (string s in Constants.lookingAngleString)
                    csv.WriteField(s);

            if (mode == Constants.eyeContourMode)
                csv.WriteField("Eye width:");
            else
                csv.WriteField("Face width:");
            //}

            csv.NextRecord();

            csv.WriteField("Picture:");
            csv.WriteField("");
            if (mode == Constants.faceElementsMode)
                csv.WriteField("");

            for (int i = 0; i < rectNames.Length; i++)
            {
                csv.WriteField("(x,");
                csv.WriteField("y)");
            }

            csv.NextRecord();

            for (int i = 0; i < realCoordinatesList.getSize(); i++)
            {
                csv.WriteField(imageNames[i]);

                if (mode != Constants.faceElementsMode)
                    csv.WriteField(elementState[i]);
                if (mode == Constants.faceElementsMode)
                {
                    foreach (U value in eyesNotVisibleContainer.getRow(i))
                        csv.WriteField(value);
                }

                foreach (T value in realCoordinatesList.getRow(i))
                    csv.WriteField(value);

                //if (mode == Constants.faceMode)
                //{
                    foreach (U value in lookAngleContainer.getRow(i))
                        csv.WriteField(value);

                    csv.WriteField(faceModeSize.getRow(i)[0]);
                //}

                csv.NextRecord();
            }

            writer.Close();
        }

        public static void writeMinMax<T, U>(char mode, CoordinatesContainer<T> minMax, CoordinatesContainer<U> faceModeMinMax = null)
        {
            bool boolMode = (mode == Constants.faceMode ? true : false);
            TextWriter writer = new StreamWriter(CaptureLabel.exportMinMaxDirectory, false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            List<List<T>> minMaxT = new List<List<T>>(minMax.getCoordinates());
            minMaxT = Enumerable.Range(0, minMaxT[0].Count)
                        .Select(i => minMaxT.Select(lst => lst[i]).ToList()).ToList();

            csv.WriteField("");

            string[] rectNames = (boolMode) ? Constants.rectangleNameF : (mode == Constants.faceElementsMode ? Constants.rectangleNameE : Constants.rectangleNameG);

            
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

                if(mode == Constants.faceMode && faceModeMinMax != null)
                    csv.WriteField(faceModeMinMax.getRow(0)[i]);

                csv.NextRecord();
                csv.WriteField("Max:");
            }

            writer.Close();
        }

        public static Tuple<List<int>, List<CoordinatesContainer<int>>> parseCSV(string path, char mode)
        {
            List<List<int>> result = new List<List<int>>();
            List<int> singleRow = new List<int>();
            int value = 0;

            Tuple<List<int>, List<CoordinatesContainer<int>>> retTuple;

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
                    result.Add(temp);
                    singleRow.Clear();
                }

                if (mode != Constants.faceElementsMode)
                    retTuple = parseTypeOneCSV(mode, result);
                else
                    retTuple = parseFaceElements(result);

                return retTuple;
            }
        }

        public static Tuple<List<int>, List<CoordinatesContainer<int>>> parseTypeOneCSV(char mode, List<List<int>> lines)
        {
            List<int> item1 = new List<int>();
            List<CoordinatesContainer<int>> item2 = new List<CoordinatesContainer<int>>();
            CoordinatesContainer<int> realCoordinates = new CoordinatesContainer<int>();
            CoordinatesContainer<int> lookAngleContainer = new CoordinatesContainer<int>();
            CoordinatesContainer<int> faceModeSize = new CoordinatesContainer<int>();

            List<int> singleRow = new List<int>();

            int iCoordLow = 0;
            int iCoordHigh = 0;

            if(mode == Constants.faceMode)
            {
                iCoordLow = 7;
                iCoordHigh = 11;
            }
            else if(mode == Constants.eyeContourMode)
            {
                iCoordLow = 11;
                iCoordHigh = 15;
            }

            //int i = 0;
            foreach (List<int> line in lines)
            {
                item1.Add(line[0]);

                for(int i = 1; i < iCoordLow/*11*/; i++)
                {
                    singleRow.Add(line[i]);
                }

                List<int> temp = new List<int>(singleRow);
                realCoordinates.addRow(temp);
                singleRow.Clear();

                for(int i = iCoordLow /*11*/; i < iCoordHigh /*15*/; i++)
                {
                    singleRow.Add(line[i]);
                }

                temp = new List<int>(singleRow);
                lookAngleContainer.addRow(temp);
                singleRow.Clear();

                singleRow.Add(line[iCoordHigh]);

                temp = new List<int>(singleRow);
                faceModeSize.addRow(temp);
                singleRow.Clear();
            }

            item2.Add(realCoordinates);
            item2.Add(lookAngleContainer);
            item2.Add(faceModeSize);
           
            return Tuple.Create(item1, item2);
        }

        public static Tuple<List<int>, List<CoordinatesContainer<int>>> parseFaceElements(List<List<int>> lines)
        {
            List<int> item1 = new List<int>();
            List<CoordinatesContainer<int>> item2 = new List<CoordinatesContainer<int>>();
            CoordinatesContainer<int> eyesNotVisibleContainer = new CoordinatesContainer<int>();
            CoordinatesContainer<int> realCoordinates = new CoordinatesContainer<int>();
            CoordinatesContainer<int> lookAngleContainer = new CoordinatesContainer<int>();
            CoordinatesContainer<int> faceModeSize = new CoordinatesContainer<int>();

            List<int> singleRow = new List<int>();

            //int i = 0;
            foreach (List<int> line in lines)
            {
                //item1.Add(line[0]);

                singleRow.Add(line[0]);
                singleRow.Add(line[1]);

                List<int> temp = new List<int>(singleRow);
                eyesNotVisibleContainer.addRow(temp);
                singleRow.Clear();

                for (int i = 2; i < 12; i++)
                {
                    singleRow.Add(line[i]);
                }

                temp = new List<int>(singleRow);
                realCoordinates.addRow(temp);
                singleRow.Clear();

                for (int i = 12; i < 16; i++)
                {
                    singleRow.Add(line[i]);
                }

                temp = new List<int>(singleRow);
                lookAngleContainer.addRow(temp);
                singleRow.Clear();

                singleRow.Add(line[16]);

                temp = new List<int>(singleRow);
                faceModeSize.addRow(temp);
                singleRow.Clear();
            }

            item2.Add(realCoordinates);
            item2.Add(lookAngleContainer);
            item2.Add(faceModeSize);
            item2.Add(eyesNotVisibleContainer);

            return Tuple.Create(item1, item2);
        }
        /*
                public static CoordinatesContainer<T> readFromCSV<T>(string path, char mode)
                {

                    CoordinatesContainer<T> result = new CoordinatesContainer<T>();
                    List<T> singleRow = new List<T>();
                    T value;

                    int start = 1;

                    using (TextReader fileReader = File.OpenText(path))
                    {
                        var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                        csv.Configuration.HasHeaderRecord = false;

                        csv.Read();
                        csv.Read();

                        if (mode == Constants.faceMode)
                            start = 2;

                        while (csv.Read())
                        {
                            for (int i = start; csv.TryGetField<T>(i, out value); i++)
                            {
                                if (mode == Constants.faceElementsMode && i == 11) break;
                                if (mode == Constants.faceMode && i == 8) break;

                                singleRow.Add(value);
                            }
                            List<T> temp = new List<T>(singleRow);
                            result.addRow(temp);
                            singleRow.Clear();
                        }

                    }
                    return result;
                }

                public static CoordinatesContainer<T> readLookAngleFromCSV<T>(string path, char mode)
                {
                    CoordinatesContainer<T> result = new CoordinatesContainer<T>();
                    List<T> singleRow = new List<T>();
                    T value;

                    int start = (mode == Constants.faceMode) ? 8 : 11;

                    using (TextReader fileReader = File.OpenText(path))
                    {
                        var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                        csv.Configuration.HasHeaderRecord = false;

                        csv.Read();
                        csv.Read();

                        while (csv.Read())
                        {
                            // correct to read look angle from face element .csv too
                            for (int i = start; csv.TryGetField<T>(i, out value) && i < start + 4; i++)
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

                public static CoordinatesContainer<T> readFaceSizeFromCSV<T>(string path, char mode)
                {

                    CoordinatesContainer<T> result = new CoordinatesContainer<T>();
                    List<T> singleRow = new List<T>();
                    T value;

                    int start = (mode == Constants.faceMode) ? 12 : 27;

                    using (TextReader fileReader = File.OpenText(path))
                    {
                        var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                        csv.Configuration.HasHeaderRecord = false;

                        csv.Read();
                        csv.Read();

                        while (csv.Read())
                        {
                            // correct to read face size from face element .csv too
                            for (int i = start; csv.TryGetField<T>(i, out value); i++)
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

                public static List<int> readIsFacePresentFromCSV(string path)
                {
                    List<int> result = new List<int>();
                    int value = 0;

                    using (TextReader fileReader = File.OpenText(path))
                    {
                        var csv = new CsvReader(fileReader, System.Globalization.CultureInfo.CurrentCulture);
                        csv.Configuration.HasHeaderRecord = false;

                        csv.Read();
                        csv.Read();

                        while (csv.Read())
                        {

                            csv.TryGetField<int>(1, out value);
                            result.Add(value);
                        }

                    }
                    return result;
                }
        */
        public static Tuple<List<List<T>>, List<List<int>>> normalizeOutput<T, U>(CoordinatesContainer<U> realCoordinatesList, CoordinatesContainer<int> faceModeSize = null, char mode = 'f')
        {
            Tuple<List<List<T>>, List<List<int>>> normalized;

            if (mode == Constants.faceMode)
                normalized = normalizeOutputFaceMode<T, U>(realCoordinatesList);
            else
                normalized = normalizeOutputFaceMode<T, U>(realCoordinatesList);

            return normalized;
        }

        public static Tuple<List<List<T>>, List<List<int>>> normalizeOutputFaceMode<T, U>(CoordinatesContainer<U> realCoordinatesList)
        {
            //CoordinatesContainer<U> retCoordinates = realCoordinatesList;

            List<List<U>> coordinates = new List<List<U>>(realCoordinatesList.getCoordinates());
            List<List<int>> minMaxValues = new List<List<int>>();
            List<List<T>> result = new List<List<T>>();

            // transpose elements
            coordinates = Enumerable.Range(0, coordinates[0].Count)
                        .Select(i => coordinates.Select(lst => lst[i]).ToList()).ToList();

            // normalize elements
            foreach (List<U> l in coordinates)
            {
                int min = Convert.ToInt32(l.Min());
                int max = Convert.ToInt32(l.Max());

                minMaxValues.Add(new List<int>() { min, max });

                List<T> temp = new List<T>();

                for (int i = 0; i < l.Count; i++)
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

        public static Tuple<List<List<T>>, List<List<int>>> normalizeOutputFaceElements<T, U>(CoordinatesContainer<U> realCoordinatesList, CoordinatesContainer<int> faceModeSize)
        {

            List<List<U>> coordinates = new List<List<U>>(realCoordinatesList.getCoordinates());
            List<List<int>> minMaxValues = new List<List<int>>();
            List<List<T>> result = new List<List<T>>();


            // normalize elements
            int i = 0;
            foreach (List<U> l in coordinates)
            {
                int faceWidth = faceModeSize.getRow(i)[0];

                List<T> temp = new List<T>();

                for (int j = 0; j < l.Count; j += 2)
                {
                    double valX = (double)(Convert.ToDouble(l[j]) / faceWidth);
                    double valY = (double)(Convert.ToDouble(l[j + 1]) / (faceWidth * Constants.modeFRectScale));

                    if (Double.IsNaN(valX) || Double.IsNaN(valY))
                    {
                        valX = 0;
                        valY = 0;
                    }
                    temp.Add((T)(object)valX);
                    temp.Add((T)(object)valY);
                }

                result.Add(temp);
                i++;
            }


            return Tuple.Create(result, minMaxValues);
        }

        public static void correctFaceCoordinates(CoordinatesContainer<int> realCoordinatesList, CoordinatesContainer<int> faceModeSize, List<double> imageResizeFactor, double scale, bool reverse = false)
        {
            int i = 0;

            // scale faceModeSize (face width) to get real coordinates of face right
            if(!reverse)
            {
                foreach (List<int> l in faceModeSize.getCoordinates())
                {
                    l[0] = (int)(Math.Round(l[0] / imageResizeFactor[i], MidpointRounding.AwayFromZero));
                    i++;
                }
            }
            
            i = 0;
            // correction factor for the first if face mode
            foreach (List<int> l in realCoordinatesList.getCoordinates())
            {
                int halfWidth = (reverse == false ? faceModeSize.getRow(i)[0] / 2 : -faceModeSize.getRow(i)[0] / 2);
                l[0] = l[0] + halfWidth;
                l[1] = l[1] + (int)(Math.Round(halfWidth * scale, MidpointRounding.AwayFromZero));
                i++;
            }

            i = 0;
            // scale faceModeSize (face width) to get relative coordinates (rectangleCoordinates) of face right
            if (reverse)
            {
                foreach (List<int> l in faceModeSize.getCoordinates())
                {
                    l[0] = (int)(Math.Round(l[0] * imageResizeFactor[i], MidpointRounding.AwayFromZero));
                    i++;
                }
            }
        
        }
    }
}
