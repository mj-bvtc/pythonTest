import time
import uuid


class Test:
    """testing a timing function"""
    def __init__(self):
        self.id = uuid.uuid4()

    @staticmethod
    def slow(self):
        for i in range(100000000):
            i * 9
        return "creamsicles!"

    @staticmethod
    def fast(self):
        for i in range(20000000):
            i/13241234
        return

    @staticmethod
    def timer(fn):
        start = time.time()
        fn()
        end = time.time()
        dur = end - start
        to_print = "Duration of function '{}' = {}".format(fn.__name__, round(dur, 2))
        print(to_print)



if __name__ == "__main__":
    t = Test()
    t.timer(t.slow)
    t.timer(t.fast)
