"""
BVTC Block object
"""
from common import Common


class Block(Common):
    def __init__(self):
        super().__init__()
        self.name = None
        self.project = None
        self.weight = None
        self.volume = None


def main():
    b = Block()
    print(b.guid)


if __name__ == "__main__":
    main()
