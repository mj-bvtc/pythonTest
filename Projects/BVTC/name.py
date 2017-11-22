"""
BVTC Block and Drop naming logic tool set.  Provides methods for
parsing through the shorthand name setting class attributes.
"""

from common import Common
import re
import pandas as pd
import numpy as np
import qr

class BlockName(Common):
    """
    BVTC Block Name/attributes
    """
    def __init__(self):
        super().__init__()
        self.style = None
        self.orientation = None
        self.length_number = None
        self.style_number = None
        self.form_method = None
        self.profile = None
        self.deleted = None
        self.phase = None
        self.size = None
        self.type = None
        self.region = None
        self.is_mirror_opposite = None
        self.notes = None
        self.repeat_number = None

    def from_shorthand(self, text):
        """
        Takes the abbreviation name and
        creates the full name attributes within the class
        :param text:
        :return:
        """
        letters = re.findall(r"[A-Za-z]+", text)
        numbers = re.findall(r"\d+", text)
        self.style = letters[0]
        self.style_number = numbers[0]
        self.orientation = letters[1] if len(letters) > 1 else None
        self.notes = letters[2:] if len(letters) > 2 else None
        self.repeat_number = re.findall(r"\((\d+)\)", text)


class DropName(Common):
    """
    Naming logic typically found on BVTC
    Agi Bumper sticker/circular 12 bit calibration
    targets.
    """
    def __init__(self):
        super().__init__()
        self.style = None
        self.orientation = None
        self.length_number = None
        self.style_number = None
        self.form_method = None
        self.profile = None
        self.deleted = None
        self.phase = None
        self.size = None
        self.type = None
        self.region = None
        self.is_mirror_opposite = None
        self.notes = None
        self.repeat_number = None
        self.floor = None
        self.drop = None
        self.drop_number = None
        self.floor_section = None
        self.block = None
        self.shorthand = None
        self.sample = None

    def from_shorthand(self, text):
        self.shorthand = text
        sections = text.split("-")
        # print(text)
        self.drop = "".join(re.findall(r"[a-zA-Z]+", sections[0]))
        self.drop_number = "".join(re.findall(r"[\d]+", sections[0]))
        self.floor = "".join(re.findall(r"[\d]+", sections[1]))
        self.floor_section = None if not sections[1] else "".join(re.findall(r"[a-zA-Z]+", sections[1]))
        self.block = "".join(sections[2:])
        self.style = get_full_name(re.findall(r"[a-zA-Z]+", self.block)[0])
        self.style_number = re.findall(r"[\d]+", self.block)[0]
        if len(sections) > 3:
            three = sections[3]
            ln = re.findall(r"^\d+", three)[0]
            # print(f"This is what I'm looking for: {ln}")
            self.length_number = ln
        if len(sections) >= 3:
            # print(f"Section two: {sections[2]}")
            two = sections[2]
            letters = re.findall(r"[a-zA-Z]+", two)
            # print(f"Letters: {letters}")
            if len(letters) >= 2:
                self.orientation = re.findall(r"^[rRlL]", letters[1])[0] if re.findall(r"^[rRlL]", letters[1]) else None
                # print(re.findall(r"^[rRlL]", letters[1]))

        self.repeat_number = re.findall(r"\((\d+)\)", text)
        self.notes = re.findall(r"[A-Za-z]+",
                                self.block)[2:] if len(re.findall(r"[A-Za-z]+", self.block)) > 2 else None
        # print(len(sections))
        third = sections[3] if len(sections) > 3 else None
        m = re.findall(r"\d+", third) if third else None
        self.length_number = m[0] if m else None


def get_full_name(name):
    name = str(name).upper()
    file = r"V:\MeshLab\_Field Survey\MK\Spreadsheets\BLOCK_STYLES.csv"
    df = pd.DataFrame.from_csv(file).reset_index(drop=False)
    result = df[df['Code'] == name]['Style'].values.tolist()  # changes ndarray to a list
    # print(df.head())
    # print(result)

    return result if result else None


def main():
    # tests = ["H1234", "H266R", "BK5", "C21L-15(2234)_SAMPLE_UPPER"]
    # b = BlockName()

    # b.from_shorthand("BK29R-2(2)_Sample_LastInLine_Lower")

    # for k, v in b.__dict__.items():
    #     print(f"{k}: {v}")
    # d = DropName()
    # d.from_shorthand("W24-51C-BK24R-2(29)_UPPER_SAMPLE")

    # name = get_full_name("AS")
    # print(name)

    tests = ["W24-51C-BK24R-87344(29)_UPPER_SAMPLE",
             "S12-5-C11",
             "E2-1C-H2(2)_SAMPLE",
             "E2-4-G1R-24566_face",
             "S1-2-E3L-4(5)"]

    for test in tests:
        d = DropName()
        d.from_shorthand(test)
        path = r"C:\Users\mkreidler\Desktop\qr_codes\\"
        data = ""
        name = str(d.guid)
        for k, v in d.__dict__.items():
            print(f"{k}: {v}")
            qr.save_qr(data, path, name)
            data += f"{k}: {v}"
            data += "\n"
        print()
        qr.save_qr(data, path, name)
        # print(f"Looking in :'{test}' orientation found: {d.orientation}")
    print("fin")


if __name__ == "__main__":
    main()

