from MyFirstPackage import TransportSystem


class Vehicle(TransportSystem.TransportDevice):
    """Something with wheels"""
    def __init__(self):
        self.name = None

    @staticmethod
    def make_noise():
        print("VROOM CHACKA VROOOMMMM")