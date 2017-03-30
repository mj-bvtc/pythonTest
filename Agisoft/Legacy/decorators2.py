import time
from functools import wraps


def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        print("Starting to wrap")
        result = fn(*args, **kwargs)
        end = time.time()
        dur = end - start
        print("Ending wrap")
        print("Duration for function '{}' is {} seconds ".format(fn.__name__, round(dur, 2)))
        return result
    return wrapper


class A(object):
    @timer
    def func(self):
        time.sleep(1)
        print("Function executing here")
        return 'func returns apple'

if __name__ == '__main__':
    log = []
    a = A()
    ret = a.func()  # works fine now
