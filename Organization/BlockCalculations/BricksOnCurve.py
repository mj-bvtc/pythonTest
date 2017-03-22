import math as m


class Data:
    """
    Stores data for block and arc

    int_angle = interior angle in degrees
    spacing = distance between block points on circle
    block_width = offsets towards arc center
    """
    def __init__(self, radius, block_length, block_width, spacing, int_angle):
        self.radius = radius
        self.block_length = block_length
        self.block_width = block_width
        self.spacing = spacing
        self.int_angle = int_angle


class BlockCurve:
    """Does various calculations for block on curve"""
    def __init__(self, data):
        self.data = data

    def get_deviation(self):
        r = self.data.radius
        leg = self.data.block_length/2
        deviation = r - m.sqrt(r**2-leg**2)
        return deviation

    def get_arc_len(self):
        angle = self.data.int_angle
        ratio = (angle/360)
        c = self.get_circumference()
        arc_len = c * ratio
        return arc_len

    def get_circumference(self):
        r = self.data.radius
        pi = m.pi
        circumference = 2 * pi * r
        return circumference

    def get_block_qty(self):
        length = self.data.block_length
        space = self.data.spacing
        nominal = length + space
        arc_len = self.get_arc_len()
        block_quantity = arc_len/nominal
        return block_quantity

    def get_bottom_space(self):
        # define variables
        r = self.data.radius  # constant
        length = self.data.block_length  # input
        w = self.data.block_width  # constant
        s = self.data.spacing  # can be input

        # solve for A
        a = m.asin((.5 * length) / r)

        # solve for C
        c = m.asin((.5 * s) / r)

        # Solve for E
        e = m.radians(90) - a - c

        # Solve for X
        x = m.cos(e) * w

        # Get Result
        space = x - (2 * x)
        return space


def main():
    for i in range(200):
        data = Data(1200, i, 12, 1, 65)
        bc = BlockCurve(data)
        print(bc.get_deviation())

if __name__ == "__main__":
    main()

