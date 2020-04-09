using System.Collections.Generic;

namespace CaptureLabel
{
    public class CoordinatesContainer
    {
        // containes all coordinates of rectangles in one picture
        private List<List<int>> rowCoordinates;

        public CoordinatesContainer()
        {
            rowCoordinates = new List<List<int>>();
        }

        public void addRow(List<int> row)
        {
            rowCoordinates.Add(row);
        }

        public void replaceRow(List<int> row, int index)
        {
            if (index < rowCoordinates.Count)
                rowCoordinates[index] = row;
        }

        public List<int> getRow(int index)
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
            List<int> row = rowCoordinates[index];

            for (int i = 0; i < row.Count; i++)
                row[i] = 0;

            replaceRow(row, index);

        }

        public List<List<int>> getCoordinates()
        {
            return rowCoordinates;
        }
    }
}
