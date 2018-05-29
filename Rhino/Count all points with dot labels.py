import rhinoscriptsyntax as rs

points = rs.GetObjects("Select points", filter=1)
point = rs.GetPoint("Place Report Dot")
rs.EnableRedraw(False)
for count, pt in enumerate(points):
    count += 1
    dot = rs.AddTextDot(count, pt)

block_count = len(points)
report_dot_text = "Total Block Count: {}".format(block_count)


rs.AddTextDot(report_dot_text, point)
rs.EnableRedraw(True)
print report_dot_text