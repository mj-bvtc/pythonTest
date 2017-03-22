import uuid


class Task:
    """
    A piece of work to be completed
    in a defined period of time
    """
    def __init__(self, name, start=None, end=None, duration=None):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.cost = None
        self.id = None
        self.isComplete = False
        self.predecessors = []
        self.resources = []
        self.subtasks = []
        self.get_duration()
        self.get_uuid()

    def get_duration(self):
        if self.end and self.start:
            dur = self.end - self.start
            self.duration = dur
            return dur

    def add_resources(self, *args):
        for resource in args:
            self.resources.append(resource)
        return

    def add_predecessors(self, *args):
        for predecessor in args:
            self.predecessors.append(predecessor)
        return

    def get_uuid(self):
        if self.id:
            return
        else:
            self.id = uuid.uuid4()
            return

    def add_subtasks(self, *args):
        for task in args:
            self.subtasks.append(task)
            return


def main():
    mb = Task("Make Breakfast", 3, 6)
    print(mb.duration)
    print(mb.id)
    mb.get_uuid()
    print(mb.id)
    mb.add_resources("tim", "bob", "joanne")
    print(mb.resources)


if __name__ == "__main__":
    main()
