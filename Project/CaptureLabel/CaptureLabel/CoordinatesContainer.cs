using System.Collections.Generic;

namespace CaptureLabel
{
    public class CoordinatesContainer<T>
    {
        // containes all coordinates of rectangles in one picture
        private List<List<T>> rowCoordinates;

        public CoordinatesContainer()
        {
            rowCoordinates = new List<List<T>>();
        }

        public CoordinatesContainer(List<List<T>> l)
        {
            rowCoordinates = new List<List<T>>(l);
        }

        public CoordinatesContainer(CoordinatesContainer<T> container)
        {
            rowCoordinates = new List<List<T>>(container.getCoordinates());
        }

        public void addRow(List<T> row)
        {
            rowCoordinates.Add(row);
        }

        public void replaceRow(List<T> row, int index)
        {
            if (index < rowCoordinates.Count)
                rowCoordinates[index] = row;
        }

        public List<T> getRow(int index)
        {
            if(index < rowCoordinates.Count)
                return rowCoordinates[index];

            return null;
        }

        public int getSize()
        {
            return rowCoordinates.Count;
        }

        public void setRowZero(int index)
        {
            List<T> row = rowCoordinates[index];

            for (int i = 0; i < row.Count; i++)
                row[i] = (T)(object)0;

            replaceRow(row, index);

        }

        public List<List<T>> getCoordinates()
        {
            return rowCoordinates;
        }
    }
}
