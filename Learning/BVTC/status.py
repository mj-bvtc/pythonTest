import common


class Status(common.Common):
    """The position of affairs at a particular time"""
    def __init__(self):
        super().__init__()
        self.task = None
        self.project = None


class Complete(Status):
    """Task/Job is done"""
    def __init__(self):
        super().__init__()
        print("Task Complete")
