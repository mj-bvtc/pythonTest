import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import importlib
import os
import PyQt5 





csv = r"C:\Users\mkreidler\Desktop\TEST.csv"
df = pd.read_csv(csv)
#print(list(df.columns.values))
print(df.columns)
