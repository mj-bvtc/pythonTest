import pandas as pd
import re


# import the excel files
ct = r"C:\Users\mkreidler\Desktop\35w\ctrac.xlsx"
rh = r"C:\Users\mkreidler\Desktop\35w\rhino.xlsx"
st = r"C:\Users\mkreidler\Desktop\35w\site.xlsx"

# convert files to dataframes
ctrac = pd.read_excel(ct)
rhino = pd.read_excel(rh)
site = pd.read_excel(st)

#remove faulty and deduct units
rhino = rhino[rhino.faulty.isna()]
rhino = rhino[rhino.deduct.isna()]


# create a new priority order
rhino["mk_priority"] = ""

rhino.loc[rhino.swing_drop == "E1", "mk_priority"] = 1
rhino.loc[rhino.swing_drop == "S1", "mk_priority"] = 2
rhino.loc[rhino.swing_drop == "S5", "mk_priority"] = 3
rhino.loc[rhino.swing_drop == "W1", "mk_priority"] = 4
rhino.loc[rhino.swing_drop == "W2", "mk_priority"] = 5
rhino.loc[rhino.swing_drop == "W3", "mk_priority"] = 6
rhino.loc[rhino.swing_drop == "S4", "mk_priority"] = 7
rhino.loc[rhino.swing_drop == "S3", "mk_priority"] = 8
rhino.loc[rhino.swing_drop == "S2", "mk_priority"] = 9

rhino = rhino.sort_values(["mk_priority","z"], ascending=[True, True])

# make a true false column based on whether or not BV surveyed
rhino["bv_survey"] = ""


def check_survey(x):
    if x not in ["S2", "S3", "S4"]:
        return True
    else:
        return False


rhino.bv_survey = rhino.swing_drop.apply(check_survey)



# create True/False column based on future work (CO11 and CO12 are not signed)

rhino["co11_12"] = ""


def find_co11_12(x):
    if x in [11, 12]:
        return True
    else:
        return False


rhino.co11_12 = rhino.co.apply(find_co11_12)




rhino = rhino.sort_values(["bv_survey", "co11_12", "mk_priority","z", "new"], ascending=[False, True, True, True, True])

rhino["ct_val"] = 1
rhino["ct_order"] = ""

rhino[["guid", "ct_val", "ct_order"]]

rhino["ct_order"] = rhino.ct_val.cumsum()

rhino[["guid", "ct_val", "ct_order"]].head()

rhino = rhino.sort_values(["bv_survey", "co11_12", "mk_priority","z", "new"], ascending=[False, True, True, True, True])