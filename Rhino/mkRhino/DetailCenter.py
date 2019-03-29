import rhinoscriptsyntax as rs
import Rhino


def DetailCenter(detail):
    box = rs.BoundingBox(detail)
    pt_set = box[0:4]
    lines = []
    
    for i, pt in enumerate(pt_set):
        if i != 3:
            line = rs.AddLine(pt, pt_set[i +1])
        else:
            line = rs.AddLine(pt, pt_set[0])
    
        lines.append(line)
    
    rect = rs.JoinCurves(lines, True)
    
    center = rs.CurveAreaCentroid(rect)[0]
    
    return center


def ObjCenter(obj):
    


def main():
    detail = rs.GetObject("Select detail view", rs.filter.detail)
    center = DetailCenter(detail)
    print center


if __name__ == "__main__":
    main()