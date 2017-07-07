import time
import datetime


print(f"time in seconds since the epoch: {time.time()}")
print(f"current date and time: {datetime.datetime.now()}")
print(f"or like this: {datetime.datetime.now().strftime('%y-%m-%d-%H-%M')}")


