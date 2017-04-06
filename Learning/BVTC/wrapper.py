def decorator(a, b, c):
    def wrap(fn):
        def wrapped_fn(*args, **kwargs):
            print(f"{a}, {b}, {c}")
            fn(*args, **kwargs)
        return wrapped_fn
    return wrap


@decorator("boy", "howdy", "mama")
def say_hello(name, num):
    exclamation = "!"*num
    print(f"Hello {name}{exclamation}")

say_hello("matt", 3)