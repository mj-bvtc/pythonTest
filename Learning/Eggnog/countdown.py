import time
import datetime

def countdown(n):
    start = datetime.datetime.now()
    while n > 0:
        print(n)
        n = n - 1
        time.sleep(1)
        if n == 0:
            end = datetime.datetime.now()
            print("Blast Off!")
            print(end - start)



countdown(720)