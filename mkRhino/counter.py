import rhinoscriptsyntax as rs


def counting(numCounts, height=1, deletePt=False):
    for i in range(numCounts):
        point = rs.GetPoint("select point")
        rs.AddPoint(point)
        count = str(i + 1)
        rs.AddText(count, point)
        
        


def main():
    counting(1000)


if __name__ == "__main__":
    main()