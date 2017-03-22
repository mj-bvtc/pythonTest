class Vehicle:
    """
    A mechanical transportation
    method
    """
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.power = None
        self.num_passengers = None
        self.passengers = None


if __name__ == "__main__":
    a = Vehicle("truck", "Berty")
    print(a.name)



