import rhinoscriptsyntax as rs
import Rhino 
import math as m


areas = [22,34,53,95,12,14,45,65,78,15,24]


area_sum = sum(areas)
num_areas = len(areas)

big_area = 45 + area_sum

square_length = m.sqrt(big_area)
big_base = square_length - 3
big_height = big_area/big_base

print big_area

big_rectangle = rs.AddRectangle(Rhino.Geometry.Plane.WorldXY, big_base, big_height)

area_4 = sum(areas[0:4])
small_base = big_base
small_height = area_4/small_base

first_w = areas[1]/small_height

rect = rs.AddRectangle(Rhino.Geometry.Plane.WorldXY, first_w, small_height)
rs.MoveObject(rect, Rhino.Geometry.Vector3d(areas[0]/small_height, 0, 0))