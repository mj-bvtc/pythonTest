using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino;
using Rhino.Geometry;

namespace BVTC.RhinoTools.Helpers
{
    public static class BoundingBox_Extensions
    {
        public static Double Measure_X(this BoundingBox bb)
        {
            // measure X dimension of a bounding box aligned to plane //
            Point3d corner = bb.Corner(true, true, true);
            return corner.DistanceTo(bb.Corner(false, true, true));
        }

        public static Double Measure_Y(this BoundingBox bb)
        {
            // measure Y dimension of a bounding box aligned to plane //
            Point3d corner = bb.Corner(true, true, true);
            return corner.DistanceTo(bb.Corner(true, false, true));
        }

        public static Double Measure_Z(this BoundingBox bb)
        {
            // measure Z dimension of a bounding box aligned to plane //
            Point3d corner = bb.Corner(true, true, true);
            return corner.DistanceTo(bb.Corner(true, true, false));
        }
    }
}
