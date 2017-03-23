def my_timer(orig_func):
    import time

    def wrapper(*args, *kwargs):
        start = time.time()
        result = orig_func(*args, **kwargs)
        dur = time.time() - start
        print('{} ran in: {} sec'.format(orig_func.__name__, dur))
        return result

    return wrapper
