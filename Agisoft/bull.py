import time


class Timer:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        start = time.time()
        print("entering {}".format(self.fn.__name__))
        result = self.fn(*args, **kwargs)
        print("exiting {}".format(self.fn.__name__))
        end = time.time()
        dur = end - start
        print("'{}' function took {} seconds to run".format(self.fn.__name__, dur))
        return result


@Timer
def hi(name, sleep):
    print("waiting {} seconds".format(sleep))
    time.sleep(sleep)
    print("hi {}".format(name))


class Apple:
    def __init__(self, name):
        self.name = name

    @Timer
    def print_name(self):
        print(name)
        return


#hi("matt", 2)

a = Apple("fred")
a.print_name()