
# coding: utf-8

# In[16]:

import uuid

class Common():
    def __init__(self):
        self.guid = uuid.uuid4()


class Project(Common):
    def __init__(self, name=None, number=None, status=None):
        super().__init__()
        self.name = name
        self.number = number
        self.status = status
        
    def get_name(self, name):
        self.name = name
    
    def get_number(self, number):
        self.number = number
        
    def get_status(self, status):
        self.status = status
    
    
projects = []
        
        
p = Project()
p.get_name("Moynihan")
p.name

p2 = Project("Woolworth", "123", "Activated")

p2.get_status("Not Active")
print(p.__dict__)
print(p2.__dict__)

projects.append(p)
projects.append(p2)

projects


# In[ ]:




# In[18]:

difficulty = 525600000000

alpha_num = 36

options = difficulty/alpha_num

options


# In[21]:

#programmatically figure out the power 36 must be raised to to get to 525 million
#this is an inprecise way, but gets the whole number (7 is not enough, and 7.5 digits does not make sense)
x = 1 
count = 0
while x < difficulty:
    x *= alpha_num
    count += 1
    print(x, count)
    
36**8


# In[23]:

##use log rules to get to decimal answer

import math as m

m.log(difficulty)/m.log(36)


# In[24]:

##cleaner way of getting decimal answer
m.log(difficulty, alpha_num)


# In[ ]:



