from common import Common


class Group(Common):
    def __init__(self, description=None, *args, **kwargs):
        super().__init__()
        self.items = [args]
        self.description = description
        # all those keys will be initialized as class attributes
        allowed_keys = set(['name', 'type', 'notes'])
        # initialize all allowed keys to false--MK made this none... because I prefer this
        self.__dict__.update((key, None) for key in allowed_keys)
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)


def main():
    g = Group("This is a description", "panda", "apple", notes="I am testing this out")
    for item in g.__dict__.items():
        print(item)


if __name__ == "__main__":
    main()
