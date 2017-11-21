from common import Common


class Project(Common):
    def __init__(self):
        super().__init__()
        self.name = None
        self.contacts = []
        self.blocks = []
        self.address = None
        self.correspondences = []
        self.samples = []


def main():
    p = Project()
    print(p.__dict__)

if __name__ == "__main__":
    main()
