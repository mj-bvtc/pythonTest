import common

block_dict = {
    "Band": "B",
    "Bracket": "BK",
    "Ashlar": "A",
    "Watertable": "W"
}

class Block(common.Common):
    """A single unit/product of masonry"""
    def __init__(self):
        super().__init__()
        self.project = None
        self.status = None
        self.style = None
        self.location = None
        self.quantity = None
        self.style_number = None
        self.orientation = None
        self.estimating_id = None
        self.region = None
        self.ornament = None
        self.form_method = None
        self.sample = None

    @property
    def block_id(self):
        prefix = block_dict[self.style]
        suffix = str(self.style_number)
        return prefix + suffix


def main():
    b = Block()
    b.style = "Watertable"
    b.style_number = 12
    print(b.block_id)

if __name__ == "__main__":
    main()
