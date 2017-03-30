import math as m

light_year_to_miles = 5.879e12
miles = 1.151e170

lys = miles/light_year_to_miles

inch = 1
foot = inch * 12
mile = foot * 5280
ly = mile * 5.879e12

print(m.log(ly, 2))
print(m.log(100, 2))

earth_radius = 20925545  # feet
bvtc_len = 1035


theta = 360 * (bvtc_len/(2 * m.pi * earth_radius))
print(theta)

pi = m.pi
r = 4
c = 2 * pi * r
c_arc = 6.283
angle = 360 * (c_arc/c)
print(angle)
