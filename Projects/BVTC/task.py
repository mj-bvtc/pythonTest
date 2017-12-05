"""
basic task that has objective and duration
"""

from common import Common
import datetime


class Task(Common):
    def __init__(self, name=None, duration=None, datetime_start=None, datetime_end=None):
        super().__init__()
        self.name = name
        self.duration = duration
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.get_duration()

    def get_duration(self):
        if (self.datetime_end is not None) & (self.datetime_start is not None):
            self.duration = self.datetime_end - self.datetime_start
        return self.duration

    def get_start_to_now(self):
        if self.datetime_start is not None:
            return datetime.datetime.now() - self.datetime_start

    def get_end_to_now(self):
        if self.datetime_end is not None:
            return datetime.datetime.now() - self.datetime_end


class Event(Common):
    """
    A defined point in time with no
    duration
    """
    def __init__(self, name=None, dt=None):
        super().__init__()
        self.name = name
        self.datetime = dt


def main():
    """
    now = datetime.datetime.now()
    birth_date = datetime.datetime(year=1991, month=12, day=7, hour=13)
    delta = now - birth_date

    bd = Event("Birth date", birth_date)

    age_years = delta.total_seconds()/60/60/365.25/24

    for k, v in bd.__dict__.items():
        print(k, v)

    print(bd.__class__.__name__)
    """
    t = Task("Clean Garage")
    t.datetime_start = datetime.datetime(2017, 10, 10)
    t.datetime_end = datetime.datetime(2018, 5, 12)

    for k, v in t.__dict__.items():
        print(k, v)


if __name__ == "__main__":
    main()
