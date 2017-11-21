from common import Common
import re


class BlockName(Common):
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
        letters = re.findall(r"[A-Za-z]+", text)
        numbers = re.findall(r"\d+", text)
        self.style = letters[0]
        self.style_number = numbers[0]
        self.orientation = letters[1] if len(letters) > 1 else None
        self.notes = letters[2:] if len(letters) > 2 else None
        self.repeat_number = re.findall(r"\((\d+)\)", text)


class DropName(Common):
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

    def from_shorthand(self, text):
        sections = text.split("-")
        print(text)
        self.drop = "".join(re.findall(r"[a-zA-Z]+", sections[0]))
        self.drop_number = "".join(re.findall(r"[\d]+", sections[0]))
        self.floor = "".join(re.findall(r"[\d]+", sections[1]))
        self.floor_section = None if not sections[1] else "".join(re.findall(r"[a-zA-Z]+", sections[1]))
        self.block = "".join(sections[2:])
        self.style = re.findall(r"[a-zA-Z]+", self.block)[0]
        self.style_number = re.findall(r"[\d]+", self.block)[0]
        self.orientation = re.findall(r"[a-zA-Z]+",
                                      sections[2])[1] if len(re.findall(r"[a-zA-Z]+", sections[2])) > 1 else None
        self.repeat_number = re.findall(r"\((\d+)\)", text)
        self.notes = re.findall(r"[A-Za-z]+",
                                self.block)[2:] if len(re.findall(r"[A-Za-z]+", self.block)) > 2 else None
        # print(len(sections))
        third = sections[3] if len(sections) > 3 else None
        m = re.findall(r"\d+", third) if third else None
        self.length_number = m[0] if m else None
        print(self.drop)
        print(self.drop_number)
        print(self.floor)
        print(self.floor_section)
        print(self.block)
        print(self.style)
        print(self.style_number)
        print(self.orientation)
        print(self.repeat_number)
        print(self.notes)
        print(self.length_number)


def main():
    # tests = ["H1234", "H266R", "BK5", "C21L-15(2234)_SAMPLE_UPPER"]
    # b = BlockName()

    # b.from_shorthand("BK29R-2(2)_Sample_LastInLine_Lower")

    # for k, v in b.__dict__.items():
    #     print(f"{k}: {v}")
    d = DropName()
    d.from_shorthand("W24-51C-BK24R-2(29)_UPPER_SAMPLE")
    # print(d.__dict__)


if __name__ == "__main__":
    main()

