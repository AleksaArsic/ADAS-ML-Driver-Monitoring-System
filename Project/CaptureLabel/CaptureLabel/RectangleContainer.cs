using System;
using System.Collections.Generic;
using System.Drawing;

namespace CaptureLabel
{
    // RectangleContainer class is used to store labeling rectangle objects and positions
    class RectangleContainer
    {
        private List<Rectangle> rectContainer = new List<Rectangle>();
        private List<bool> rectFocusList = new List<bool>();

        // constructor used for face elements mode
        public RectangleContainer()
        {
            for (int i = 0; i < Constants.faceElementStartPos.Length; i += 2)
            {
                rectContainer.Add(new Rectangle(new Point(Constants.faceElementStartPos[i], Constants.faceElementStartPos[i + 1]), Constants.rectSize));
                rectFocusList.Add(false);
            }
        }

        // constructor used for face mode
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

        // constructor that accepts array of sizes to be set to corresponding rectangle
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

        // get stored rectangle objects as Rectangle[]
        public Rectangle[] getRectangles()
        {
            return rectContainer.ToArray();
        }

        // get stored rectangle objects as List<Rectangle> 
        public List<Rectangle> getRectangles(int a)
        {
            return rectContainer;
        }

        // get number of stored rectangles
        public int getSize()
        {
            return rectContainer.Count;
        }

        // set size to rectangle at index index
        public void setRectSize(int index, Size size)
        {
            // check if index is valid
            if (index >= rectContainer.Count)
                return;

            Rectangle rect = rectContainer[index];
            rect.Size = size;

            rectContainer[index] = rect;
        }

        // get stored rectangle coordinates as List<int>
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

        // set rectangle coordinates at index index
        public void setRectCoordinates(int index, int x, int y)
        {
            Rectangle rect = rectContainer[index];

            rect.X = x;
            rect.Y = y;

            rectContainer[index] = rect;
        }

        // set all rectangle coordinates to List<int> coordinates
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

        // check if rectangle is in focus
        public bool isInFocus(Rectangle r)
        {
            // check if rectangle exists 
            if (rectContainer.Contains(r))
            {
                return rectFocusList[rectContainer.IndexOf(r)];
            }
                
            return false;
        }

        // set focus to rectangle at index index
        public void setFocus(int index)
        {
            rectFocusList[index] = !rectFocusList[index];
        }

        // set focus to rectangle r
        public void setFocus(Rectangle r)
        {
            // check if rectangle exists 
            if(rectContainer.Contains(r))
            {
                rectFocusList[rectContainer.IndexOf(r)] = !rectFocusList[rectContainer.IndexOf(r)];
            }
        }

        // check if Point p is in some rectangle
        public Tuple<bool, int> contains(Point p)
        {
            // iterate trough rectangle list and check if the point is on some rectangle
            foreach(Rectangle r in rectContainer)
            {
                if (r.Contains(p))
                    return Tuple.Create(true, rectContainer.IndexOf(r));
            }

            return Tuple.Create(false, -1);
        }

        // find rectangle in focus
        public Rectangle findInFocus()
        {
            // iterate trough rectangles and find one in focus if any
            for(int i = 0; i < rectFocusList.Count; i++)
            {
                if(rectFocusList[i])
                {
                    return rectContainer[i];
                }
            }

            return Rectangle.Empty;
        }

        // get index of rectangle that is in focus
        public int inFocusIndex()
        {
            // iterate trough rectangles and return index of one in focus if any
            for (int i = 0; i < rectFocusList.Count; i++)
            {
                if (rectFocusList[i])
                {
                    return i;
                }
            }

            return -1;
        }

        // add x and y distance to focused rectangle
        public void addToFocused(int x, int y)
        {
            int focusedIndex = inFocusIndex();

            Rectangle rect = rectContainer[focusedIndex];

            rect.X += x;
            rect.Y += y;

            rectContainer[focusedIndex] = rect;
        }

        // reset foucs list 
        // after this function is executed there is no rectangle in focus
        public void resetFocusList()
        {
            for(int i = 0; i < rectFocusList.Count; i++)
            {
                rectFocusList[i] = false;
            }
        }

        // reset coordinates of all rectangles
        public void resetCoordinates(int[] position)
        {
            int j = 0;

            // iterate trough rectangles and reset their position to int[] position
            for (int i = 0; i < rectContainer.Count * 2; i += 2, j++)
            {
                Rectangle rect = rectContainer[j];

                rect.X = position[i];
                rect.Y = position[i + 1];

                rectContainer[j] = rect;
            }
        }

        // increase or decrease size of rectangle
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

        // rescales rectangle at index index to constant width and height with factor
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

        // reset whole class 
        public void resetState(char mode, int[] position)
        {
            resetFocusList();
            resetCoordinates(position);
        }
    }
}
