import rhinoscriptsyntax as rs
import Rhino



def mid_letter(curve, letter):
    height = 3
    point = rs.CurveMidPoint(curve)
    rs.AddText(letter, point, height, justification=131074)

def get_curves():
    curves = rs.GetObjects("Select all curves", rs.filter.curve)
    return curves

def format_label(prefix, count, length):
    label = "{}{}= {}'".format(prefix,count, length)
    return label


def main():
    curves = get_curves()
    file = open("C:\Users\mkreidler\Desktop\CinUnionTerm_Measures2.txt", "w")
    file.write("BVTC_Cincinnati Union Terminal Survey\n")
    file.write("Measurements\n")
    count = 1
    for curve in curves:
        length = round(rs.CurveLength(curve),2)
        label = format_label("AA", count, length)
        file.write(label)
        file.write("\n")
        mid_letter(curve, label)
        count += 1
        
    file.close()

if __name__ == "__main__":
    main()