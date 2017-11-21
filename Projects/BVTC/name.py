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


tests = ["H1234", "H266R", "BK5", "C21L-15(2234)_SAMPLE_UPPER"]
b = BlockName()

b.from_shorthand("BK29R-2(2)_Sample_LastInLine_Lower")

for k, v in b.__dict__.items():
    print(f"{k}: {v}")



