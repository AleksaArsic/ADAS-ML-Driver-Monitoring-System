using System;
using System.Collections.Generic;
using System.Linq;

namespace CaptureLabel
{
    // RectangleContainer<T> generic class is used to store List of Lists<T>
    public class CoordinatesContainer<T>
    {
        // containes all coordinates of rectangles in one picture
        private List<List<T>> rowCoordinates;

        // Constructor
        public CoordinatesContainer()
        {
            rowCoordinates = new List<List<T>>();
        }

        // Constructor with parameter l that is a List of Lists<T>
        public CoordinatesContainer(List<List<T>> l)
        {
            rowCoordinates = new List<List<T>>(l);
        }

        // copy constructor
        public CoordinatesContainer(CoordinatesContainer<T> container)
        {
            rowCoordinates = new List<List<T>>(container.getCoordinates());
        }

        // add row of coordinates to CoordinatesContainer object
        public void addRow(List<T> row)
        {
            rowCoordinates.Add(row);
        }

        // replace row of coordinates in CoordinatesContainer object
        public void replaceRow(List<T> row, int index)
        {
            if (index < rowCoordinates.Count)
                rowCoordinates[index] = row;
        }

        // get row of coordinates from CoordinatesContainer object at index index
        public List<T> getRow(int index)
        {
            if(index < rowCoordinates.Count)
                return rowCoordinates[index];

            return null;
        }

        // get size of CoordinatesContainer object
        public int getSize()
        {
            return rowCoordinates.Count;
        }

        // set row of coordinates to 0
        public void setRowZero(int index)
        {
            List<T> row = rowCoordinates[index];

            // iterate trough row and set it to zero for every value
            for (int i = 0; i < row.Count; i++)
                row[i] = (T)(object)0;

            replaceRow(row, index);

        }

        // return List of Lists<T> associated with CoordinatesContainer object
        public List<List<T>> getCoordinates()
        {
            return rowCoordinates;
        }

        // change type from T to U 
        public List<List<U>> ConvertTo<U>()
        {
            List<List<U>> result = new List<List<U>>();

            // iterate trough rows of rowCoordinates and cast them from type T to type U
            foreach (List<T> row in rowCoordinates)
                result.Add(row.Cast<object>().Select(x => (U)Convert.ChangeType(x, typeof(U))).ToList());

            return result;
        }
    }
}
