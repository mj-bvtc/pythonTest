import uuid


class Common:
    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        self.value = 5

    def auto_attr(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Fish(Common):
    def __init__(self, **kwargs):
        self.name = None
        super().__init__()
        self.value += 2
        self.auto_attr(kwargs)

    def talk(self):
        if not self.name:
            print("No name given")
        else:
            print(f"Hello, my name is {self.name}")

    def add_name(self, name):
        self.name = name
        print(f"Name '{name}' added to object")


class Shark(Fish):
    def __init__(self, **kwargs):
        super().__init__()
        self.value = self.value // 3
        self.auto_attr(kwargs)


f = Fish(name="simon")
s = Shark(name="bologna")

print(s.id)
# s.add_name("Jerry")
s.talk()

print(s.value)
print(s.__dict__)
