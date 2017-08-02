def block_volume(length, width, height, number_walls, thickness):
    l, w, h, n, t = length, width, height, number_walls, thickness
    face = w * l * t
    top_bottom = 2 * ((h-t)*l*t)
    walls = n*((h - t)*t*(w-(2*t)))
    volume = face + top_bottom + walls
    return volume


def bounding_box_volume(length, width, height):
    return length*width*height


block = block_volume(20, 8, 10, 3, 1.25)
box = bounding_box_volume(20, 8, 10)
ratio = block/box
print(ratio)