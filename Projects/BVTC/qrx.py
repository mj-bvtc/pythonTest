import pandas as pd
from common import Common
import re
import tkinter
from tkinter.filedialog import askopenfilename
import math as m
import name_tools


class Quote(Common):
    def __init__(self):
        super().__init__()      # adds common attributes like time_created
        self.file = None        # save location
        self.df = None          # main DataFrame to be carried/updated throughout process
        self.df_original = None # original DataFrame
        self.get_file()         # tkinter UI to browse for files
        self.import_data()      #
        self.molds_df = None

    def get_file(self):
        """
        Simple UI browser to get CSV file generated in
        Bluebeam.  Gets file path.
        """
        tkinter.Tk().withdraw()
        self.file = askopenfilename()

    def import_data(self):
        """
        Imports CSV into Pandas DataFrame
        """
        self.df = pd.DataFrame.from_csv(self.file).reset_index()
        self.df_original = self.df

    @property
    def project_number(self):
        """
        Gets project number if present
        """
        pnum = self.df[["Project #"]]
        pnum = pnum.dropna()

        try:
            return pnum['Project #'].iloc[0]
        except [Exception, FileNotFoundError]:
            return None

    @property
    def by_phase_id(self):
        """
        Returns DataFrame grouped by Phase and Estimating ID
        """
        return self.df[['Phase', 'Estimating ID', '# Units']].groupby(['Phase', 'Estimating ID']).sum().reset_index()

    @property
    def unique_df(self):
        """
        Gets clean df for combine_data
        """
        data = self.df.drop_duplicates(subset="Estimating ID", keep='first')
        data = data.drop(["Phase", "# Units", "Project #"], axis=1)
        return data

    @property
    def combine_data(self):
        """Combines sums into main df"""
        self.df = self.by_phase_id.merge(self.unique_df, on="Estimating ID", how="left")
        return self.df

    @property
    def rename_columns(self):
        """Renames columns as estimating desires"""
        self.df = self.combine_data.rename(columns={"Estimating ID": "Block ID",
                                                    "Cost Per Model": "$/Model",
                                                    "Cost Per Mold": "$/Mold",
                                                    "Cost Per Unit": "$/Unit"})
        return self.df

    @property
    def add_dwgs(self):
        """Tallies the number of drawings per style"""
        def num_dwg(x):
            result = 1
            try:
                hyphen = re.findall(r"-(\d+)", str(x))
                result = 0 if int(hyphen[0]) > 1 else 1
            finally:
                return result

        df2 = self.rename_columns
        df2["# DWGs"] = df2["Block ID"].apply(num_dwg)
        self.df = df2
        return self.df

    def export(self):
        """Generates CSV of self.df, saves in same folder as Raw data"""
        self.df.to_csv(self.export_name)

    @property
    def export_name(self):
        """Formats a new save name, adding timestamp to avoid naming collisions"""
        name = str(self.file)
        name = name.replace(".csv", "")
        dt = self.time_created.strftime("%Y%m%d%H%M%S")
        name = name + dt + ".csv"
        return name

    @property
    def add_total_unit_cost(self):
        """Calculates total unit cost"""
        def remove_dollar(x):
            return float(x.replace("$", ""))
        self.df["Total Unit $"] = self.df["# Units"] * self.df["$/Unit"].apply(remove_dollar)
        return self.df

    def calculate_molds(self):
        """
        Broken:  calculates number of molds per style
        requires logic to work by phase then block id
        also needs to account for project running total

        ex: Phase 1 [a1 x10, a1-1 x1]   requires 1 mold
            Phase 2 [a1 x1]             requires 0 molds (use Phase 1)
            Phase 3 [a1-3 x13]          requires 2 molds (Phase 1 mold retired]
        """
        def get_base(x):
            # base = same profile, same style and style number
            style = re.findall(r"[a-zA-Z]+", x)[0]
            style_num = re.findall(r"[\d]+", x)[0]
            return style + style_num
        base = self.df  # copy the dataframe
        base["base"] = base["Block ID"].apply(get_base)  # add a base column, populate fields
        # print(base)
        sums = base[["base", "# Units", "Phase"]].groupby(["Phase", "base"]).sum()  # calculate total of each base style
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
        # df = self.df.copy()
        # get a list of base styles
        # df = df[["Block ID", "# Molds", "base"]]
        df = self.df

        def fx(text):
            b = name_tools.Block(text)
            c = b.length_number if b.length_number else 0
            return int(c)

        df["len_num"] = df["Block ID"].apply(fx)
        # print(df)
        # base_list = list(set(self.df["base"].values))
        # base_list.sort()
        # only the lowest numbered hyphenated style gets sum, rest get zero
        # print(base_list)

        # df["# Molds"] = 0 if df["len_num"] > 1 else df["# Molds"]
        df["repeat"] = df.groupby(["Phase", "base"]).cumcount() + 1

        def test(repeat, mold):
            if repeat > 1:
                return 0
            else:
                return mold
        # https://stackoverflow.com/questions/16353729/pandas-how-to-use-apply-function-to-multiple-columns
        df["# Molds"] = df.apply(lambda x: test(x["repeat"],
                                                   x["# Molds"]), axis=1)  # needs work


        print(df)


    @staticmethod
    def get_length_number(_text):
        pattern = r"-(\d+)"
        result = re.findall(pattern, _text)
        if result:
            return result[0]
        else:
            return None

    def run(self):
        self.add_dwgs
        self.add_total_unit_cost
        self.calculate_molds()
        self.remove_duplicate_molds()
        self.export()

    def run2(self):
        self.add_dwgs()

def main():
    q = Quote()
    q.run()


if __name__ == "__main__":
    main()
