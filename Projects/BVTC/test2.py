from common import Common


class Bird(Common):
    def __init__(self):
        super().__init__()


b = Bird()
print(b.time_created)
