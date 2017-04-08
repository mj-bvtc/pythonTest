import pandas as pd
import matplotlib.pyplot as plt

age = 25
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24
year = day * 365

sec_per_year = year
min_per_year = year/60

forester = 25000
payback = 36
money_down = 4000


def monthly_payments(cost, pay_period, down_payment, apr):
    payment = round((cost - down_payment)/pay_period, 2)
    print(f"You will be paying ${payment} per "
          f"month for {payback} months on your {cost} loan")
    return payment

monthly_payments(forester, payback, money_down, 4)
monthly_payments(25000, 60, 2000, 10)
