using System;
using System.Collections.Generic;
using System.Drawing;

namespace CaptureLabel
{
    class RectangleContainer
    {
        private List<Rectangle> rectContainer = new List<Rectangle>();
        private List<bool> rectFocusList = new List<bool>();

        public RectangleContainer()
        {
            for (int i = 0; i < Constants.faceElementStartPos.Length; i += 2)
            {
                rectContainer.Add(new Rectangle(new Point(Constants.faceElementStartPos[i], Constants.faceElementStartPos[i + 1]), Constants.rectSize));
                rectFocusList.Add(false);
            }
        }
        public RectangleContainer(int rectNo, int[] startPos, Size rectSize)
        {
            if (rectNo > startPos.Length)
                return;

            int j = 0;
            for (int i = 0; i < rectNo * 2; i += 2, j++)
            {
                rectContainer.Add(new Rectangle(new Point(startPos[i], startPos[i + 1]), rectSize));
                rectFocusList.Add(false);
            }
        }

        public RectangleContainer(int rectNo, int[] startPos, Size[] rectSize)
        {
            if (rectNo > startPos.Length)
                return;

            int j = 0;
            for(int i = 0; i < rectNo * 2; i += 2, j++)
            {
                rectContainer.Add(new Rectangle(new Point(startPos[i], startPos[i + 1]), rectSize[j]));
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

        public void setRectSize(int index, Size size)
        {
            if (index >= rectContainer.Count)
                return;

            Rectangle rect = rectContainer[index];
            rect.Size = size;

            rectContainer[index] = rect;
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

        public void resetCoordinates(char mode)
        {
            int j = 0;

            int[] rectSLocation = (mode == 'f') ? Constants.faceModeStartPos : Constants.faceElementStartPos;

            for (int i = 0; i < rectContainer.Count * 2; i += 2, j++)
            {
                Rectangle rect = rectContainer[j];

                rect.X = rectSLocation[i];
                rect.Y = rectSLocation[i + 1];

                rectContainer[j] = rect;
            }
        }

        public void addToRectSize(int index, int width, int height)
        {
            Rectangle rect = rectContainer[index];

            // minimal size is 5px
            if (rect.Width > 5)
            {
                rect.Width += width;
                rect.Height = height;
            }

            rectContainer[index] = rect;
        }

        public void rescaleRect(int index, int width, double factor)
        {
            Rectangle rect = rectContainer[index];

            // minimal size is 5px
            if (rect.Width > 5)
            {
                rect.Width += width;
                rect.Height = (int)(Math.Ceiling(rect.Width * factor));
            }

            rectContainer[index] = rect;
        }


        public void resetState(char mode)
        {
            resetFocusList();
            resetCoordinates(mode);
        }
    }
}
