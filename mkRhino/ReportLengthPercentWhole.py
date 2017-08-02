import rhinoscriptsyntax as rs
import Rhino


#get curves
crvs = rs.GetObjects("Get curves to measure", rs.filter.curve)

overall_len = sum([rs.CurveLength(x) for x in crvs])
print overall_len

for crv in crvs:
    cl = round(rs.CurveLength(crv), 3)
    percent = round((cl/overall_len) * 100, 2)
    print "This curve is {} inches long and is {}% of the combined length".format(cl, percent)

