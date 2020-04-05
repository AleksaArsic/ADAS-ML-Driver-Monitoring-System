using System;
using System.Collections.Generic;
using System.Drawing;

namespace CaptureLabel
{
    class RectangleContainer
    {
        private List<Rectangle> rectContainer = new List<Rectangle>();
        private List<bool> rectFocusList = new List<bool>();

        private Size rectSize = new Size(10, 10);

        private readonly int[] rectStartLoc =
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

        public static readonly string[] names =
            {"LE Up", "LE Down", "LE Left", "LE Right", "RE Up", "RE Down", "RE Left", "RE Right",
               "Nose", "Mouth Up", "Mouth Down"};

        public RectangleContainer()
        {
            for (int i = 0; i < rectStartLoc.Length; i += 2)
            {
                rectContainer.Add(new Rectangle(new Point(rectStartLoc[i], rectStartLoc[i + 1]), rectSize));
                rectFocusList.Add(false);
            }
        }

        public Rectangle[] getRectangles()
        {
            return rectContainer.ToArray();
        }

        public List<Rectangle> getRectangles(int a)
        {
            return rectContainer;
        }

        public int getSize()
        {
            return rectContainer.Count;
        }

        public List<int> getAllRectCoordinates()
        {
            List<int> coordinates = new List<int>();

            foreach(Rectangle r in rectContainer)
            {
                coordinates.Add(r.X);
                coordinates.Add(r.Y);
            }

            return coordinates;
        }

        public void setRectCoordinates(int index, int x, int y)
        {
            Rectangle rect = rectContainer[index];

            rect.X = x;
            rect.Y = y;

            rectContainer[index] = rect;
        }

        public void setAllRectCoordinates(List<int> coordinates)
        {
            int j = 0;
            for(int i = 0; i < coordinates.Count; i += 2, j++)
            {
                Rectangle rect = rectContainer[j];

                rect.X = coordinates[i];
                rect.Y = coordinates[i + 1];

                rectContainer[j] = rect;
            }
        }

        public bool isInFocus(Rectangle r)
        {
            if (rectContainer.Contains(r))
            {
                return rectFocusList[rectContainer.IndexOf(r)];
            }
                

            return false;
        }

        public void setFocus(int index)
        {
            rectFocusList[index] = !rectFocusList[index];
        }

        public void setFocus(Rectangle r)
        {
            if(rectContainer.Contains(r))
            {
                rectFocusList[rectContainer.IndexOf(r)] = !rectFocusList[rectContainer.IndexOf(r)];
            }
        }

        public Tuple<bool, int> contains(Point p)
        {
            foreach(Rectangle r in rectContainer)
            {
                if (r.Contains(p))
                    return Tuple.Create(true, rectContainer.IndexOf(r));
            }

            return Tuple.Create(false, -1);
        }

        public Rectangle findInFocus()
        {

            for(int i = 0; i < rectFocusList.Count; i++)
            {
                if(rectFocusList[i])
                {
                    return rectContainer[i];
                }
            }

            return Rectangle.Empty;
        }

        public int inFocusIndex()
        {
            for (int i = 0; i < rectFocusList.Count; i++)
            {
                if (rectFocusList[i])
                {
                    return i;
                }
            }

            return -1;
        }

        public void addToFocused(int x, int y)
        {
            int focusedIndex = inFocusIndex();

            Rectangle rect = rectContainer[focusedIndex];

            rect.X += x;
            rect.Y += y;

            rectContainer[focusedIndex] = rect;
        }

        public void resetFocusList()
        {
            for(int i = 0; i < rectFocusList.Count; i++)
            {
                rectFocusList[i] = false;
            }
        }

        public void resetCoordinates()
        {
            int j = 0;

            for (int i = 0; i < rectStartLoc.Length; i += 2, j++)
            {
                Rectangle rect = rectContainer[j];

                rect.X = rectStartLoc[i];
                rect.Y = rectStartLoc[i + 1];

                rectContainer[j] = rect;
            }
        }

        public void resetState()
        {
            resetFocusList();
            resetCoordinates();
        }
    }
}
