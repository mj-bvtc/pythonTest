import os
import platform
import datetime
import time


def get_user():
    return os.getenv('username')


def get_machine():
    return platform.node()


def get_user_machine():
    uam = "{}@{}".format(get_user(), get_machine())
    return uam


def get_datetime():
    return datetime.datetime.now()


def get_log_stamp():
    return "{} {}".format(get_user_machine(), get_datetime())


def timer(seconds, fn):
    now = time.time()
    stop = now + seconds
    count = 1
    print("Start: {}".format(datetime.datetime.now().time()))
    while time.time() < stop:
        fn()
        count += 1
    print("Stop: {}".format(datetime.datetime.now().time()))
    print("Count: {}".format(count))


def main():
    # print get_log_stamp()
    # timer(2, get_log_stamp)
    pass


if __name__ == "__main__":
    main()
