import time

log = ["\n"]


def my_timer(orig_func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = orig_func(*args, **kwargs)
        dur = time.time() - start
        message = '{} ran in: {} sec'.format(orig_func.__name__, round(dur, 2))
        print(message)
        log.append(message)
        return result

    return wrapper


class DecoratorClass(object):
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print('call method ')
        return self.original_function(*args, **kwargs)


@DecoratorClass
def test(seconds):
    time.sleep(seconds)
    print(list(i for i in range(0, 10)))
    print(f"I slept for {seconds} seconds!")
    return seconds


@my_timer
def test2(seconds):
    time.sleep(seconds)
    print(f"I slept for {seconds} seconds!")
    return seconds


def main():
    test(1)
    test2(2)
    for msg in log:
        print(msg)

if __name__ == "__main__":
    main()
