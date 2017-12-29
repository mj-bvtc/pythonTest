"""
BVTC common object
"""
import uuid
import os
import platform
import datetime


def get_user():
    return os.getenv('username')


def get_machine():
    return platform.node()


def get_datetime():
    return datetime.datetime.now()


class Common:
    def __init__(self):
        self.guid = uuid.uuid4()
        self.user = get_user()
        self.machine = get_machine()
        self.time_created = get_datetime()


def main():
    c = Common()
    print(c.__dict__)


if __name__ == "__main__":
    main()
