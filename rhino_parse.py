
# coding: utf-8


import pandas as pd
import numpy as np
import re

###
###
### IMPORT RAW DATA
###
###


# import the excel file
rh = r"C:\Users\mkreidler\Desktop\35w\rhino.xlsx"


# convert files to dataframes
rhino = pd.read_excel(rh)




df = rhino




# clean data
df.x = pd.to_numeric(df.x)
df.y = pd.to_numeric(df.y)
df.z = pd.to_numeric(df.z)

# creating the framework
df["new"] = ""
df["co"] = ""
df["priority_ctrac"] = ""
df["swing_drop"] = ""
df["faulty"] = ""
df["remediation"] = ""
df["deduct"] = ""
df["floor"] = ""
df["elevation"] = ""
df["project"] = ""
rhino["bv_survey"] = ""
rhino["co11_12"] = ""
rhino["mk_priority"] = ""
rhino["ct_val"] = 1
rhino["ct_order"] = ""

# creating definitions
df.new = df.layer.apply(lambda x: "NEW" in str(x))   #this defines and executes at once
def find_co(x):
    pat = r"CO[\s]*([0-9]+)"
    result = re.search(pat, str(x))
    if result:
        return int(result.group(1))
    
def find_priority(x):
    pat = r"P([0-9]+)"
    result = re.search(pat, str(x))
    if result:
        return int(result.group(1))  

def get_drop(x):

    pat = r"drop\s*([a-z]*\d*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        #print("Found Match")
        return match.group(1)
    else:
        #print("Not Found")
        return None

def find_faulty(x):
    pat = r"faulty"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return "faulty"
    
def find_remediation(x):
    pat = r"remediation"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return "re"

def find_deduct(x):
    pat = r"deduct"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return "deduct"
    
def find_floor(x):
    pat = r"floor\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))
    
def find_elevation(x):
    pat = r"([a-zA-Z]*)\s*ELEVATION"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return result.group(1)

    
def find_project(x):
    pat = r"'project\s+(.*)'"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return result.group(1)
    else:
        print("not in project")
        
        
def check_survey(x):
    if x not in ["S2", "S3", "S4"]:
        return "bv_surveyed"
    else:
        return "survey required"

    
def find_co11_12(x):
    if x in [11, 12]:
        return "in scope"
    else:
        return "NIS"

# executing the functions to parse/assign data
df.co = df.layer.apply(find_co)
df.priority_ctrac = df.layer.apply(find_priority)
df.swing_drop = df.zones.apply(get_drop)
df.faulty = df.layer.apply(find_faulty)
df.remediation = df.layer.apply(find_remediation)
df.deduct = df.layer.apply(find_deduct)
df.floor = df.zones.apply(find_floor)
df.elevation = df.zones.apply(find_elevation)
df.project = df.zones.apply(find_project)
df.bv_survey = df.swing_drop.apply(check_survey)
df.co11_12 = df.co.apply(find_co11_12)


# assign the mk method of sorting drops
df.loc[df.swing_drop == "E1", "mk_priority"] = 1
df.loc[df.swing_drop == "S1", "mk_priority"] = 2
df.loc[df.swing_drop == "S5", "mk_priority"] = 3
df.loc[df.swing_drop == "W1", "mk_priority"] = 4
df.loc[df.swing_drop == "W2", "mk_priority"] = 5
df.loc[df.swing_drop == "W3", "mk_priority"] = 6
df.loc[df.swing_drop == "S4", "mk_priority"] = 7
df.loc[df.swing_drop == "S3", "mk_priority"] = 8
df.loc[df.swing_drop == "S2", "mk_priority"] = 9

#sort values and hold that order with cumsum()
df = df.sort_values(["bv_survey", "co11_12", "mk_priority","z", "new"], ascending=[True, False, True, True, True])
df["ct_order"] = df.ct_val.cumsum()






