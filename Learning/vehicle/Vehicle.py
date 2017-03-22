import uuid


class Vehicle(object):
    """
    A mechanical transportation
    method
    """
    def __init__(self, type, name):
        self.id = uuid.uuid4()
        self.type = type
        self.name = name
        self.power = None
        self.num_passengers = None
        self.passengers = None


# TODO inherit vehicle into a child class
class Truck(Vehicle):
    """
    Vehicle that performs work and transports
    passengers
    """

    def __init__(self, name):
        Vehicle.__init__(self, "Truck", name)
        self.is_4x4 = None
        self.bed_area = 32


def hello(name):
    print(f"Hello {name}!")
    return

if __name__ == "__main__":
    a = Vehicle("truck", "Berty")
    print(a.name)
    b = Truck("ben")
    msg1 = (f"{b.name.title()} is a {b.type.lower()} "
            f"with a bed area of {b.bed_area} square feet")
    msg2 = (f"{b.name.title()}'s id is {b.id}")

    print(msg1, len(msg1))
    print(msg2, len(msg2))



