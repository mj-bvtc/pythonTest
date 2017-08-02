import time
import datetime
import uuid
import sympy


class Common:
    def __init__(self):
        self.id = uuid.uuid4()
        self.start = datetime.datetime.now()


class Action(Common):
    def __init__(self, action):
        super().__init__()
        self.employee = []
        self.action = action
        self.location = None
        self.end = None
        self.blocks = []

    def action_complete(self):
        self.end = datetime.datetime.now()

    @property
    def duration(self):
        return self.end - self.start


class Employee(Common):
    number = 0

    def __init__(self, name, title):
        super().__init__()
        self.name = name
        self.title = title
        Employee.number += 1
        self.enum = Employee.number


class Block(Common):
    def __init__(self, name):
        super().__init__()
        self.project = None
        self.name = name
        self.type = None
        self.size = None
        self.body = None
        self.kiln_schedule = None
        self.quantity = None


class Group(Common):
    def __init__(self):
        super().__init__()
        self.group = []

    def add(self, items):
        self.group.extend(items)


def main():
    bk = Block("BK24")
    bk.project = "P14-0509"
    a = Block("A12")
    a.project = "P12-3456"

    matt = Employee("Matthew", "developer")
    ron = Employee("Ronald", "surveyor")
    survey = Action("Site Survey")
    survey.blocks = [bk, a]
    time.sleep(.125)
    survey.action_complete()
    print(survey.duration)
    print(survey.id)
    survey.employee = [matt, ron]

    print(survey.__dict__)
    print(matt.number)
    print(matt.enum)

    for e in survey.employee:
        print(e.name)

    print(survey.start)
    print(matt.start)

    x, y, z = sympy.symbols('x y z')
    print(sympy.diff(sympy.cos(x), x))

if __name__ == "__main__":
    main()
