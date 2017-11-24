import rhinoscriptsyntax as rs
import Rhino

x,y,z = 0.1875, 0.1875, 0
offset = 3/16
i = [x,y,z]
dx = 2 + 13/16
dy = 1.375
matrix = [3,8]

for col in range(matrix[0]):
    for row in range(matrix[1]):
        x,y,z = 0.1875, 0.1875, 0
        print "Col:{}, Row{}".format(col, row)
        img = r"C:\Users\mkreidler\Desktop\qr_codes\88f8aec2-3d55-4d79-962e-91a574c62b9a.png"

        nx = x + (dx*col) 
        ny = y + (dy*row)
        nz = 0
        pt1 = [nx, ny, nz]
        pt2 = [nx+1, ny, nz]
        rs.AddPoint(pt1)
        rs.AddPoint(pt2)
        print pt1
        print pt2
        cmd = "-PictureFrame "
        cmd += img
        cmd += " "
        cmd += ",".join([str(x) for x in pt1])
        cmd += " "
        cmd += ",".join([str(x) for x in pt2])
        cmd += " "
        rs.Command(cmd)
        
