import pandas as pd
from common import Common
import re
import tkinter
from tkinter.filedialog import askopenfilename
import os
import datetime
import math as m
from name import BlockName

class Quote(Common):
    def __init__(self):
        super().__init__()
        self.file = None
        self.df = None
        self.df_original = None
        self.get_file()
        self.import_data()
        self.molds_df = None

    def get_file(self):
        tkinter.Tk().withdraw()
        self.file = askopenfilename()

    @property
    def by_style(self):
        return self.df[['Estimating ID', '# Units']].groupby("Estimating ID").sum()

    def import_data(self):
        self.df = pd.DataFrame.from_csv(self.file).reset_index()
        self.df_original = self.df

    @property
    def project_number(self):
        pnum = self.df[["Project #"]]
        pnum = pnum.dropna()
        # nulls = pnum.isnull()
        # not_null = pnum.notnull()
        return pnum['Project #'].iloc[0]

    @property
    def by_phase_id(self):
        return self.df[['Phase', 'Estimating ID', '# Units']].groupby(['Phase', 'Estimating ID']).sum().reset_index()

    @property
    def header_original(self):
        # header = list(df)
        return ['Project #', 'Phase', 'Phase #', 'Deleted', 'Client ID', 'Estimating ID',
                'Description', 'Type', 'Ornament', 'Size', 'Page Label', 'Form Method',
                '# Units', 'Cost Per Model', 'Cost Per Mold', 'Cost Per Unit']

    @property
    def header_output(self):
        # header = list(df)
        return ['Phase', "Block ID", "Description", "#DWGs", "Form Method",
                "New Dies", "Existing Dies", "# Models", "# Molds", "$/Model",
                "$/Mold", "$ New Die", "Existing Die", "# Units", "$/Unit", "Total Unit $"]

    @property
    def combine_data(self):
        self.df = self.by_phase_id.merge(self.unique_df, on="Estimating ID", how="left")
        return self.df

    @property
    def unique_df(self):
        data = self.df.drop_duplicates(subset="Estimating ID", keep='first')
        data = data.drop(["Phase", "# Units", "Project #"], axis=1)
        return data

    @property
    def rename_columns(self):
        self.df = self.combine_data.rename(columns={"Estimating ID": "Block ID",
                                                 "Cost Per Model": "$/Model",
                                                 "Cost Per Mold": "$/Mold",
                                                 "Cost Per Unit": "$/Unit"})
        return self.df

    @property
    def add_dwgs(self):
        def num_dwg(x):
            result = 1
            try:
                hyphen = re.findall(r"-(\d+)", str(x))
                result = 0 if int(hyphen[0]) > 1 else 1
            finally:
                return result

        df2 = self.rename_columns
        df2["#DWGs"] = df2["Block ID"].apply(num_dwg)
        self.df = df2
        return self.df

    def export(self):
        self.df.to_csv(self.export_name)

    @property
    def export_name(self):
        name = str(self.file)
        name = name.replace(".csv", "")
        dt = self.time_created.strftime("%Y%m%d%H%M%S")
        name = name + dt + ".csv"
        return name

    @property
    def add_total_unit_cost(self):
        def remove_dollar(x):
            return float(x.replace("$", ""))
        self.df["Total Unit $"] = self.df["# Units"] * self.df["$/Unit"].apply(remove_dollar)
        return self.df

    def calculate_molds(self):
        def get_base(x):
            # base = same profile, same style and style number
            style = re.findall(r"[a-zA-Z]+", x)[0]
            style_num = re.findall(r"[\d]+", x)[0]
            return style + style_num
        base = self.df  # copy the dataframe
        base["base"] = base["Block ID"].apply(get_base)  # add a base column, populate fields
        # print(base)
        sums = base[["base", "# Units"]].groupby("base").sum()  # calculate total of each base style
        # sums = sums.merge(base, on="base", how="left")

        def div_12_round(x):
            return m.ceil(x/12)
        sums["# Molds"] = sums["# Units"].apply(div_12_round)  # div 12, round up = how many molds we get per unit
        self.molds_df = sums
        sums.reset_index(inplace=True)  # index seems to mess up merge, re indexing fixes this
        self.df = self.df.merge(sums[["base", "# Molds"]],
                                on="base", how="left", copy=False)  # This duplicates summed values per style, error
        # print(sums)

    def remove_duplicate_molds(self):
        df = self.df
        # get a list of base styles
        df = df[["Block ID", "# Molds"]]
        # print(df)

        base_list = list(set(self.df["base"].values))
        base_list.sort()
        # only the lowest numbered hyphenated style gets sum, rest get zero
        # print(base_list)




    def run(self):
        self.add_dwgs
        self.add_total_unit_cost
        self.calculate_molds()
        self.remove_duplicate_molds()
        # self.export()


def main():
    # q = Quote()
    bn = BlockName()
    bn.from_shorthand("W1-1")
    print(bn.length_number)



if __name__ == "__main__":
    main()

