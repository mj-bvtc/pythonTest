
# coding: utf-8

# In[8]:

import datetime
import time
import pandas as pd
import re

class Mold:
    def __init__(self, units=0, inventory=0, log=True):
        self.presses_per_mold = 12
        self.log = log
        self.units_log = []
        self.presses = []
        self.mold_purchases = []
        self.remaining_presses = []
        self.tot_press = []          #amount of presses if you maxed out molds
        self.timestamps = []
        
    def write_log(self, x=None):
        if self.log:
            print(x)
        
    def request_units(self, units):
        self.units_log.append(units)
        self.write_log(f"{units} units requested and added to log")
        self.check_inventory()
        self.buy_molds()
        self.get_remaining_presses()
        now = datetime.datetime.now()
        self.timestamps.append(now)
        
    def get_remaining_presses(self):
        press = sum(self.presses)
        units = sum(self.units_log)
        delta = press - units
        self.remaining_presses.append(delta)
        tot = self.units_log[-1] + (self.remaining_presses[-1])
        self.tot_press.append(tot)

    def check_inventory(self):
        if sum(self.units_log) > sum(self.presses):
            self.write_log("You need to buy mold(s)")
        else:
            diff = sum(self.presses) - sum(self.units_log)
            self.write_log(f"You have {sum(self.presses)} presses and {sum(self.units_log)} units")
            self.write_log(f"You have {diff} presses remaining")
            print()
    
    def buy_molds(self):
        if sum(self.units_log) > sum(self.presses):
            delta = sum(self.units_log) - sum(self.presses)
            buy = self.calculate_molds(delta)
            self.write_log(f"I bought {buy} mold(s)")
            self.write_log()
            self.mold_purchases.append(buy)
            press = buy * self.presses_per_mold
            self.presses.append(press)
        else:
            self.mold_purchases.append(0)
            self.presses.append(0)
            
    
    def calculate_molds(self, units):
        result = ((units - 1)//self.presses_per_mold) + 1
        return result
    
    @property
    def df(self):
        result = None
        try:
            d = {"Requested Units": self.units_log,
                 "Purchased Presses": self.presses,
                 "Purchased Molds": self.mold_purchases,
                 "Leftover Presses": self.remaining_presses,
                 "Total Available Presses": self.tot_press,
                 "DT": self.timestamps}
            df = pd.DataFrame(data=d)
            result = df[["Requested Units", 
                         "Purchased Molds", 
                         "Purchased Presses",
                         "Total Available Presses", 
                         "Leftover Presses"]]
        finally:
            return result



# In[9]:

file = r"C:\Users\mkreidler\Desktop\dump\test.csv"
raw = pd.DataFrame.from_csv(file)
raw.reset_index(inplace=True)
df = raw.copy()


def clean(df):
    #remove dollar signs
    df["Cost Per Model"] = df["Cost Per Model"].str.replace("$", "")
    df["Cost Per Unit"] = df["Cost Per Unit"].str.replace("$", "")
    df["Cost Per Mold"] = df["Cost Per Mold"].str.replace("$", "")

    df["Cost Per Model"] = df["Cost Per Model"].str.replace(",", "")
    df["Cost Per Unit"] = df["Cost Per Unit"].str.replace(",", "")
    df["Cost Per Mold"] = df["Cost Per Mold"].str.replace(",", "")

    #string to numeric
    pd.to_numeric(df["Cost Per Model"])
    pd.to_numeric(df["Cost Per Mold"])
    pd.to_numeric(df["Cost Per Unit"])

    return df

def rename(df):
    #rename columns
    df  = df.rename(columns={ "Estimating ID": "Block ID",
                        "Cost Per Model": "$/Model",
                        "Cost Per Mold": "$/Mold",
                        "Cost Per Unit": "$/Unit"})
    return df

def add_base(df):
    import name_tools as nt

    #add base name
    def fx(x):
        b = nt.Block(x)
        base = b.style + b.style_number
        return base
    
    df["base"] = df["Block ID"].apply(fx)
    df[["Phase", "Block ID", "base"]].head()
    
    return df

def run(df):
    df = clean(df)
    df = rename(df)
    df = add_base(df)
    return df
df = run(df)
col = ["Phase", "Block ID", "base", "# Units"]   
df[col].head()


# In[10]:

#group list
tot = df.groupby(["Phase", "base"]).sum()
tot = tot.drop(["Client ID", "Phase #"], axis=1)
tot.reset_index(inplace=True)

#get unique base names
base_list = set(tot["base"].tolist())

#create dictionary of molds per base name
base_dict = {}
for b in base_list:
    k = b
    v = Mold(log=False)     #####set this to False to suppress printing
    base_dict[k] = v
    
base_dict


# In[11]:

tot.head()


# In[12]:

#tot["# Molds"] = base_dict[tot["base"]].(tot["# Units"])

def get_mold_num(base, units):
    base_dict[base].request_units(units)    
    result = base_dict[base].mold_purchases[-1]
    #print(base_dict[base].df)
    return result

tot["# Molds"] = tot.apply(lambda x: get_mold_num(x["base"], x["# Units"]), axis=1)
#tot
    
print(tot)


# In[14]:

#get_ipython().magic('ls')


# In[ ]:






# In[ ]:



