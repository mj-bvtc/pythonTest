import common


class Project(common.Common):
    """A defined job with a scope of work and end goal"""
    def __init__(self):
        super().__init__()
        self.number = None
        self.name = None
        self.status = None
        self.address = None
        self.scale = None

