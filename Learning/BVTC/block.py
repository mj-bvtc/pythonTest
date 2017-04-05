import common


class Block(common.Common):
    """A single unit/product of masonry"""
    def __init__(self):
        super().__init__()
        self.project = None
        self.status = None
        self.block_type = None
        self.location = None
