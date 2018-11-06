import rhinoscriptsyntax as rs


def dot_count(start, end, increment):
    for i in range(start, end, increment ):
        point = rs.GetPoint("Pick a point")
        rs.AddTextDot(i, point)

dot_count(20, 40, 1)