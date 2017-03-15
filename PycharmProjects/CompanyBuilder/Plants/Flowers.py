class Flower(object):
    def __init__(self, number_petals, color):
        self.number_petals = number_petals
        self.color = color
        self.age = None
        self.dirt_condition = "Decent"
        self.height = None


    def touchPetals(self):
        for petal in range(self.number_petals):
            print('ooh that is soft')


class Rose(Flower):
    def __init__(self, number_thorns):
        self.number_thorns = number_thorns
        Flower.__init__(self, 25, "Red")


def main():
    my_flower = Rose(22)
    print(my_flower.number_thorns)
    print(my_flower.age)
    my_flower.age = 4
    print(my_flower.age)

    print(my_flower.dirt_condition)

    my_flower.dirt_condition = "the best!"
    print(my_flower.dirt_condition)
    print(my_flower.__dict__)
    my_flower.touchPetals()
    lily = Flower(2, "white")
    print(lily.number_petals)
    lily.touchPetals()

if __name__ == "__main__":
    main()
