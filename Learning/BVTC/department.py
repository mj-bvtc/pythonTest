import common
import business
import status


class Department(common.Common):
    """A subset of a business with a specific goal"""
    def __init__(self):
        super().__init__()
        self.name = None
        self.employees = []
        self.tasks = []
        self.biz = None


class BostonDepartment(Department):
    def __init__(self):
        super().__init__()
        self.biz = business.BVTC


class MeshLab(BostonDepartment):
    def __init__(self):
        super().__init__()

