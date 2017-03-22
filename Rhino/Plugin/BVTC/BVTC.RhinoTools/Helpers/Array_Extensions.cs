using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace BVTC.RhinoTools.Helpers
{
    public static class Array_Extensions
    {
        public static T[] SubArray<T>(this T[] data, int index, int length)
        {
            /* Helper method to create a sub-array 
             */
            T[] result = new T[length];
            Array.Copy(data, index, result, 0, length);
            return result;
        }
    }
}
