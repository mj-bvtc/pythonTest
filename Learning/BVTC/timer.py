from functools import wraps
import time


def timer(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # print("instance {} of class {} is decorated".format(self, self.__class__))
        # print("entering...")
        # print("running process...")
        start = time.time()
        result = fn(self, *args, **kwargs)
        end = time.time()
        # print("exiting...")
        dur = end - start
        msg = "'{}' function took {} seconds to run\n\n".format(fn.__name__, round(dur, 2))
        print(msg)
        self.log_list.append(msg)  # send log to class????
        return result
    return wrapper
