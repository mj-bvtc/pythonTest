class NoiseMaker(object):
    def __init__(self):
        self.noise = None
        self.name = None

    def make_noise(self):
        print(f"A wild {self.name} makes a {self.noise} sound!")


