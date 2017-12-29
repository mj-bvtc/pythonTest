import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Rate:
    warren = 95
    matt = 20
    per_diem = 75
    hotel = 100
    taxi = 40
    air_fare = 200


class Job:
    def __init__(self, work_days=None):
        self.work_days = work_days
        self.travel_days = None
        self.get_travel_days()

    def get_travel_days(self):
        self.travel_days = (((self.work_days-1)//3)*2)+2
        return self.travel_days

    def get_cost(self, rate):
        travel_pay = self.travel_days * rate * 6
        travel_fare = self.travel_days * Rate.air_fare
        work_pay = self.work_days * rate * 8
        per_diem = Rate.per_diem
        taxi = Rate.taxi * (self.work_days + self.travel_days)
        total = travel_pay + work_pay + per_diem + travel_fare + taxi
        return total

    def get_cost_warren_nyc(self, rate):
        travel_pay = self.travel_days * rate * 6
        work_pay = self.work_days * rate * 8
        per_diem = Rate.per_diem
        total = travel_pay + work_pay + per_diem
        return total


# nyc = Job(7)
# cost_m = nyc.get_cost(Rate.matt)
# cost_w = nyc.get_cost(Rate.warren)
# print(cost_m * 2)
# print(cost_w)

x = [num for num in range(1, 14, 1)]
matt = [Job(a).get_cost(Rate.matt) for a in x]
two_bvtc = [Job(a).get_cost(Rate.matt)*2 for a in x]
warren = [Job(a).get_cost(Rate.warren) for a in x]
warren_nyc = [Job(a).get_cost_warren_nyc(Rate.warren) for a in x]

plt.plot(x, matt, label="Matt")
plt.plot(x, warren, label="Warren")
plt.plot(x, two_bvtc, label="Two BVTC")
plt.plot(x, warren_nyc, label="Warren NYC")
plt.legend()
plt.plot()
plt.show()
# plt.savefig(r"C:\Users\mkreidler\Desktop\warren_matt_2bvtc_comparison3.svg", dpi=1200, format="svg")

