using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CaptureLabel
{
    class Utilities
    {
        public static readonly String[] supportedFormats = { ".jpeg", ".jpg", ".png" };

        public List<string> parseImagesToList(List<string> inList)
        {
            List<string> outList = new List<string>();

            foreach (string item in inList)
            {
                for (int i = 0; i < supportedFormats.Length; i++)
                {
                    if (item.Contains(supportedFormats[i]))
                    {
                        outList.Add(item);
                        break;
                    }
                }
            }

            return outList;
        }
    }
}
