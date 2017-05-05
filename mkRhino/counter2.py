import rhinoscriptsyntax as rs
import thread, time

def addCount(count):
    pt = rs.GetPoint("Click to add a count")
    point = rs.AddPoint(pt)
    rs.AddText(str(count), point)

def counting(keepCount):
    count = 1
    while keepCount:
        addCount(count)
        count +=1

counting(True)