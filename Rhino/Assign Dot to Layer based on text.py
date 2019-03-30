# -*- coding: utf-8 -*-
import pandas as pd

# excel file to reference, color assignments from Nikola
file = r"V:\Projects\Shell House Building\TerraCotta\_Preliminary_Models\Color Assignment\Shell Color Assignment.xlsx"

# convert the excel file into a pandas dataframe
df = pd.read_excel(file)

# function to test excel line item exists in rhino setting
def check(test):
    if test in text:
        return True

    else:
        return False

# function to grab the guid for rhino object
def get_id(test):
    if test in text:
        i = text.index(test)
        return id[i]        

# use check function on all lines in dataframe
# check if excel line exists in rhino setting 
df["in"] = df["name"].map(check)

# pare down data to only items that exist in setting and rhino
data = df[df["in"] == True]
data["guid"] = df["name"].map(get_id)



#csv file report
data.to_csv("V:\Projects\Shell House Building\TerraCotta\_Preliminary_Models\Color Assignment\ShellColorLocations.csv")

#resulting lists of rhino objects and 
guid_list = data.guid.tolist()
layer = data.color.tolist()

#status complete
print("Script Complete")

  