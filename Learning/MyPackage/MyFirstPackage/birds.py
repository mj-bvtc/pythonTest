from MyFirstPackage import noiseMakers, flyers


class Bird(noiseMakers.NoiseMaker, flyers.Flyers):
    def __init__(self, noise, name):
        super().__init__()
        self.noise = noise
        self.name = name
        self.wing_size = None


b = Bird("cachicachica", "smorg")
b.make_noise()
b.fly()
b.wing_size = "pretty huge"
