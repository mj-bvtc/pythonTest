import uuid


class Common:
    """Common base class amongst all classes"""
    def __init__(self):
        self.id = uuid.uuid4()
