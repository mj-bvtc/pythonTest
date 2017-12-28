from Projects.BVTC.common import Common


class Egg(Common):
    def __init__(self):
        super().__init__()


def get_travel_days(work_days):
    return (((work_days-1)//3)*2)+2


my_list = [1, 2, 3, 4]
my_list.pop(2)
print(my_list)
e = Egg()
print(e.time_created)