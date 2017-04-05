import common
import department


class Task(common.Common):
    """A piece of work to be undertaken"""
    def __init__(self):
        super().__init__()
        self.name = None
        self.due_date = None
        self.start_date = None
        self.manager = None
        self.employees = []
        self.department = None


class RunAgi(Task):
    def __init__(self):
        super().__init__()
        self.department = department.MeshLab
        self.name = "RunAgi"
        self.due_date = 20170407
