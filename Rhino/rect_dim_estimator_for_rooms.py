import rhinoscriptsyntax as rs
import Rhino

curve = rs.GetObject("select rectangle")
rect = rs.ExplodeCurves(curve)

d1 = rs.CurveLength(rect[0])
d2 = rs.CurveLength(rect[1])

dims = [d1, d2]

center = rs.CurveAreaCentroid(curve)
print center

if d1 == d2:
    print "square"
else:
    message =  "{} by {}".format(int(round(max(dims))),int(round(min(dims))))
    rs.AddText(message, center[0], justification=131074)

def round_unit(num):
    return int(round(num))

def estimate(nums, high=True):
    if high:
        return round_unit(max(nums))
    else:
        return round_unit(min(nums))
