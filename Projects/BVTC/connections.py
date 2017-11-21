from common import Common


class Connections(Common):
    def __init__(self, a=None, b=None):
        self.a = a.guid
        self.b = b.guid


class Test(Common):
    def __init__(self):
        super().__init__()


class Toast(Common):
    def __init__(self):
        super().__init__()


def main():
    t = Test()
    tt = Toast()
    c = Connections(t, tt)
    print(c.__dict__)


if __name__ == "__main__":
    main()
