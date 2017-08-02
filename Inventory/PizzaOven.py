import math as m
import pint

def sphere_volume(r):
    return (4/3)*m.pi*(r**3)


def cylinder_volume(r, h):
    return m.pi*(r**2)*h

outer = sphere_volume(18)
inner = sphere_volume(17)
dome = (outer - inner)/2

big_cyl = cylinder_volume(9, 12)
small_cyl = cylinder_volume(8, 12)
door = (big_cyl - small_cyl)/2


def cubic_inch_to_gallon(cubic_inch):
    return cubic_inch*.004329

cub_inch = dome + door
gal_clay = cubic_inch_to_gallon(cub_inch)


print(gal_clay)

