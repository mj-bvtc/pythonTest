class Task:
    """A clear objective with a start and end date"""

    def __init__(self, title, objective, start=None, end=None, duration=None, complete=False):
        self.title = title
        self.objective = objective
        self.start = start
        self.end = end
        self.duration = duration
        self.resources = []
        self.cost = None
        self.get_duration()
        self.complete = complete

    def get_duration(self):
        if self.start and self.end:
            duration = self.end - self.start
            self.duration = duration
            return duration

    def add_resource(self, *args):
        for count, thing in enumerate(args):
            print("{0}. {1}".format(count, thing))
            self.resources.append(thing)


def main():
    rebuild = Task("Rebuild", "Rebuild the broken windows in the office", 2, 531)
    print(rebuild.duration)
    rebuild.add_resource("Frank", "Benny", "Jets")
    print(rebuild.resources)

if __name__ == "__main__":
    main()
