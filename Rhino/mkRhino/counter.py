import rhinoscriptsyntax as rs


def counting(numCounts, height=1, deletePt=False, start=0):
    for i in range(numCounts):
        point = rs.GetPoint("select point")
        #rs.AddPoint(point)
        count = str(i +start)
        rs.AddTextDot("FLOOR "+count, point)
        
        


def main():
    counting(21, start=1)


if __name__ == "__main__":
    main()