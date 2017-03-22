class Cake(object):
    def __init__(self, numberCakes):
        self.base = "flour"
        self.liquid = "water"
        self.sweet = "sugar"
        self.glue = "egg"
        self.numCakes = numberCakes


class Pancake(Cake):
    def __init__(self):
        super
        self.size = "large"
        self.structure = "flat"


class Waffle(Cake):
    def __init__(self, num_cakes):
        super().__init__(num_cakes)
        self.size = "medium"
        self.structure = "grid"


def main():
    waffle = Waffle(7)
    print(waffle.numCakes)


if __name__ == "__main__":
    main()
