import os
import platform
import datetime
import RandomColor
import imp 

hello = imp.load_source('hello', r"V:\MeshLab\_FieldSurvey\MK\python\pythonTest\Agisoft\hello.py")



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


def main():
    print get_log_stamp()
    print RandomColor.rand_color()
    print hello.greeting()


if __name__ == "__main__":
    main()
