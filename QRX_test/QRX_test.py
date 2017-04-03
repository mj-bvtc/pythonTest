import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv = r"V:\Projects\770 Broadway\_Field Work\Corner Change Order\770Broadway_ChangeOrderCorner.csv"
fields = ["Survey ID", "# Units"]
df = pd.read_csv(csv, skipinitialspace=True, usecols=fields)
cols = df.columns

df.to_html("example.html")


