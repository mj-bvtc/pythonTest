
# coding: utf-8

# In[35]:

import math as m
import time
import pint

def sphere(radius):
    return 4/3*m.pi*radius**3

ureg = pint.UnitRegistry()
radius = 16 * ureg.inch

t = 15*ureg.second

print(radius)
print(radius.to(ureg.meter))
sp = sphere(radius).to(ureg.gallon)

gps = sp/t
print(gps)

half_sphere = sp/2 #this is a half a sphere, in gallons

print(round(half_sphere.to(ureg.cu_ft),4))
print(half_sphere.to(ureg.cu_ft))

print(half_sphere.to_base_units())
print(round(half_sphere.to(ureg.gallon)/(5*ureg.foot), 1))



# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



