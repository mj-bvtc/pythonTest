#!/usr/bin/env python
# coding: utf-8

# In[61]:


import random
import datetime
from pygame import mixer 
import time


def correct():
    mixer.init()
    mixer.music.load("/home/cole/Music/sounds/335908__littlerainyseasons__correct.mp3")
    #mixer.music.load("/home/cole/Music/sounds/352659__foolboymedia__alert-chime-1.mp3")
    mixer.music.play()	
    print("Correct!\n")

def wrong():
    mixer.init()
    #mixer.music.load("/home/cole/Music/sounds/335908__littlerainyseasons__correct.mp3")
    mixer.music.load("/home/cole/Music/sounds/352659__foolboymedia__alert-chime-1.mp3")
    mixer.music.play()	
    print("Try again please...\n")

def any_digit(log=None):
    a = random.randint(1,999)
    b = random.randint(1,999)
    
    start = datetime.datetime.now()
    print(f"\n\nAdd these:\n\n{a:{10}}\n{b:{10}}\n")
    
    user_answer = int(input("Your answer:"))
    
    """
    if user_answer == a+b:
        print("Correct!")
        
    else:
        print("try again")
        
    """
    attempts = 1
    while user_answer != (a + b):
        wrong()
        user_answer = int(input("Your answer:"))
        attempts += 1

    if user_answer == (a+b):
        correct()

    
    print("************************\n")
    end = datetime.datetime.now()
    duration = end - start
    
    print()
    print(f"Clocked at: {duration}")
    print(f"Attempts: {attempts}")
    if log:
        log.write(f"{a},{b},{a+b},{duration},{attempts}\n")
    
# width = 10
# precision = 4
# value = decimal.Decimal('12.34567')
# f'result: {value:{width}.{precision}}'
# 'result:      12.35'


def num_questions(num, log=None):
    for i in range(num):
        any_digit(log=log)
    print()
    time.sleep(2)


log_path = r"/home/cole/Desktop/log2.txt"    

with open(log_path, 'a') as log:
    log.write("\n")
    log.write("Matt's Math Game\n")
    log.write(f"Date: {datetime.datetime.now()}\n")
    log.write("\n") 
    log.write("Adding a + b, from 1 to 99\n")
    log.write("a,b,answer,duration, attempts\n")
    num = int(input("How many questions would you like?"))
    num_questions(num, log=log)
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




