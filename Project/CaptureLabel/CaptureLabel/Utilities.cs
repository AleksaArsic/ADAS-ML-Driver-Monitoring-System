using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using CsvHelper;

namespace CaptureLabel
{
    // static class used for various methods used by application
    static class Utilities
    {
        // parse supported image formats locations to List<string>
        public static List<string> parseImagesToList(List<string> inList)
        {
            List<string> outList = new List<string>();

            // loop trough everything in folder that's already been stored in List<string> inList
            foreach (string item in inList)
            {
                // loop trough inList and check if there are any images with supported formats
                for (int i = 0; i < Constants.supportedFormats.Length; i++)
                {
                    if (item.Contains(Constants.supportedFormats[i]))
                    {
                        // add it to supported formats list
                        outList.Add(item);
                        break;
                    }
                }
            }

            return outList;
        }

        // switch mode based on ToolStripMenuItem[] tsmi list
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

        // write relevant information to .csv file that is not normalized
        public static void writeToCSV<T, U, X>(char mode, CoordinatesContainer<T> realCoordinatesList, List<string> imageNames, 
                                                CoordinatesContainer<U> lookAngleContainer, CoordinatesContainer<X> faceModeSize, 
                                                List<int> elementState = null, CoordinatesContainer<U> eyesNotVisibleContainer = null, bool normalized = false)
        {
            // should be embedded in try-catch
            string csvPath = (normalized == true ? CaptureLabel.exportDirectory : CaptureLabel.saveDirectory);
            TextWriter writer = new StreamWriter(@csvPath, false, Encoding.UTF8);
            CsvSerializer serializer = new CsvSerializer(writer, System.Globalization.CultureInfo.CurrentCulture);
            CsvWriter csv = new CsvWriter(serializer);

            csv.WriteField("");

            string[] rectNames = ((mode == Constants.faceMode) ? Constants.rectangleNameF : (mode == Constants.faceElementsMode ? Constants.rectangleNameE : Constants.rectangleNameG));

            // construct header
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

            foreach (string s in Constants.lookingAngleString)
                csv.WriteField(s);

            if (mode == Constants.eyeContourMode)
                csv.WriteField("Eye width:");
            else
                csv.WriteField("Face width:");

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

            // write rectangle coordinates to .csv file based on mode
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

                foreach (U value in lookAngleContainer.getRow(i))
                    csv.WriteField(value);

                csv.WriteField(faceModeSize.getRow(i)[0]);


                csv.NextRecord();
            }

            writer.Close();
        }

        // write minimal and maximal values of coordinates used for normalization and denormalization of data 
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

            // check which mode is selected to construct appropriate header
            string[] rectNames = (boolMode) ? Constants.rectangleNameF : (mode == Constants.faceElementsMode ? Constants.rectangleNameE : Constants.rectangleNameG);
            
            // construct header
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

            // write minimal and maximal values to .csv file
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

        // parse input .csv file that is passed to .csv path text box
        public static Tuple<List<int>, List<CoordinatesContainer<int>>> parseCSV(string path, char mode)
        {
            List<List<int>> result = new List<List<int>>();
            List<int> singleRow = new List<int>();
            int value = 0;
            // construct Tuple object that contains List<int> with relevant information of the current mode 
            // and List<CoordinateContainer<int>> that contains coordinates 
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

                // based on working mode parse values 
                if (mode != Constants.faceElementsMode)
                    retTuple = parseTypeOneCSV(mode, result);
                else
                    retTuple = parseFaceElements(result);

                return retTuple;
            }
        }

        // used for parsing face elements mode and eye contour mode .csv files
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

            // sets starting reading positions base on the working mode
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

            // interate rough rows of values and parse them appropriately 
            foreach (List<int> line in lines)
            {
                item1.Add(line[0]);

                for(int i = 1; i < iCoordLow; i++)
                {
                    singleRow.Add(line[i]);
                }

                List<int> temp = new List<int>(singleRow);
                realCoordinates.addRow(temp);
                singleRow.Clear();

                for(int i = iCoordLow; i < iCoordHigh; i++)
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

        // parsing face elements mode values from .csv file
        public static Tuple<List<int>, List<CoordinatesContainer<int>>> parseFaceElements(List<List<int>> lines)
        {
            List<int> item1 = new List<int>();
            List<CoordinatesContainer<int>> item2 = new List<CoordinatesContainer<int>>();
            CoordinatesContainer<int> eyesNotVisibleContainer = new CoordinatesContainer<int>();
            CoordinatesContainer<int> realCoordinates = new CoordinatesContainer<int>();
            CoordinatesContainer<int> lookAngleContainer = new CoordinatesContainer<int>();
            CoordinatesContainer<int> faceModeSize = new CoordinatesContainer<int>();

            List<int> singleRow = new List<int>();

            // interate rough rows of values and parse them appropriately 
            foreach (List<int> line in lines)
            {
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

        // called as part of the private void exportNormalized() function
        // normalize output values to be saved to new .csv file
        public static Tuple<List<List<T>>, List<List<int>>> normalizeOutput<T, U>(CoordinatesContainer<U> realCoordinatesList, CoordinatesContainer<int> faceModeSize = null, char mode = 'f')
        {
            Tuple<List<List<T>>, List<List<int>>> normalized;

            if (mode == Constants.faceMode)
                normalized = normalizeOutputFaceMode<T, U>(realCoordinatesList);
            else
                normalized = normalizeOutputFaceMode<T, U>(realCoordinatesList);

            return normalized;
        }

        // normalize output values for face mode 
        public static Tuple<List<List<T>>, List<List<int>>> normalizeOutputFaceMode<T, U>(CoordinatesContainer<U> realCoordinatesList)
        {
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

                // normalize output with formula:
                // Xnorm = (X - Xmin) / (Xmax - Xmin)
                for (int i = 0; i < l.Count; i++)
                {
                    double val = (double)(Convert.ToInt32(l[i]) - min) / (max - min);

                    // if value is not a number set it to zero
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

        // normalize output values for face elements and eye countour mode
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

                // normalize output with formula:
                // Xnorm = (X - Xmin) / (Xmax - Xmin)
                for (int j = 0; j < l.Count; j += 2)
                {
                    double valX = (double)(Convert.ToDouble(l[j]) / faceWidth);
                    double valY = (double)(Convert.ToDouble(l[j + 1]) / (faceWidth * Constants.modeFRectScale));

                    // if value is not a number set it to zero
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

        // correct face rectangle coordinates because stored coordinates are coordinates
        // of top left corner of the rectangle and we need central point for neural network input
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
