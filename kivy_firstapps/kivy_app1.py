#!/usr/bin/env python
# -*- encoding: utf-8

import datetime
import pandas as pd
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import dfgui
import pandas as pd
from kivy.properties import ObjectProperty

###########


def find_all(style, rnd):
    # file = r"V:\Projects\35 East Wacker\Field Work\BVTC Survey #2\35 Wacker -- Measurement DB.xlsx"
    file = r"V:\Projects\35 East Wacker\Field Work\BVTC Survey #2\SPREADSHEET STYLE GUIDE -MAB compiled.xlsx"
    # df = pd.read_excel(file, sheet_name= "Main")
    df = pd.read_excel(file)
    cols = ["family", "description", "name", "length", "height", "depth", "note", "dwg"]

    df.length = df.length.fillna(0)
    df.height = df.height.fillna(0)
    df.depth = df.depth.fillna(0)

    def my_round(x, rnd=rnd):
        """Takes some floating point number
        and rounds to closest base"""
        return rnd * round(x / rnd)

    def clean(x):
        return x.strip()

    df.family = df.family.apply(clean)
    m = df.loc[df.family == style, cols]

    m["L"] = m.length.apply(my_round)
    m["H"] = m.height.apply(my_round)
    m["D"] = m.depth.apply(my_round)

    m = m.sort_values(["length", "height", "depth", "name"])

    return m


def find_match(style, rnd=1 / 8, L=0, H=0, D=0):
    df = find_all(style, rnd)
    if L + H + D == 0:
        return df

    def my_round(x, rnd=rnd):
        """Takes some floating point number
        and rounds to closest base"""
        return rnd * round(x / rnd)

    L = my_round(L, rnd)
    H = my_round(H, rnd)
    D = my_round(D, rnd)

    print(L, H, D)

    df = df.loc[df.L == L, :]
    df = df.loc[df.H == H, :]
    # df = df.loc[df.D == D, :]
    return df[["family", "description", "name", "length", "height", "depth", "note", "dwg"]]


find_match(style="ashlar",
           rnd=1,
           L=21,
           H=12,
           D=4)


# result = find_all("band", rnd=1/8)
# result.loc[result.name == "4A11", :]

############

class Wacker(App):
    def build(self):
        return GraphDraw()

class GraphDraw(GridLayout):
    #style = ObjectProperty(None)
    #length = ObjectProperty(None)
    #height = ObjectProperty(None)
    #depth = ObjectProperty(None)

    def graph(self):
        file = r"V:\Projects\35 East Wacker\Field Work\BVTC Survey #2\SPREADSHEET STYLE GUIDE -MAB compiled.xlsx"
        df = pd.read_excel(file)
        #xls = pd.read_excel('filepath')
        #df = pd.DataFrame.xls
        dfgui.show(df)
        #print xls





if __name__ == '__main__':
    Wacker().run()