import re
from common import Common


class Block(Common):
    def __init__(self, text):
        self.input = text
        self.style = get_style(text)
        self.style_number = get_style_number(text)
        self.orientation = get_orientation(text)
        self.length_number = get_length_number(text)
        self.notes = get_notes(text)

    def report(self):
        print(f"Style: {self.style}\n "
              f"Style Number: {self.style_number}\n "
              f"Orientation: {self.orientation}\n "
              f"Length Number: {self.length_number}\n "
              f"Notes: {self.notes}")


def get_length_number(text):
    """
    Returns first group of letters,

    """
    pattern = r"-(\d+)"
    result = re.findall(pattern, text)
    if result:
        return result[0]
    else:
        return None


def get_style(text):
    pattern = r"[a-zA-Z]+"
    result = None
    try:
        result = re.findall(pattern, text)[0]

    finally:
        return result


def get_orientation(text):
    pattern = r"[a-zA-Z]+[\d]+([rRlL]+)"
    result = None
    try:
        result = re.findall(pattern, text)[0]

    finally:
        return result


def get_style_number(text):
    pattern = r"[a-zA-Z]+([\d]+)"
    result = None
    try:
        result = re.findall(pattern, text)[0]

    finally:
        return result


def get_notes(text):
    pattern = r"[a-zA-Z]+[\d]+[rRlL]*[-]*[\d]+(.*)"
    result = None
    try:
        result = re.findall(pattern, text)
        if result:
            back = []
            for r in result:
                a = re.sub(r"[-_]", " ",r)
                b = str(a).strip()
                back.append(b)
            result = back

    finally:
        return result


def report(tests):
    for t in tests:
        style = get_style(t)
        style_number = get_style_number(t)
        orientation = get_orientation(t)
        length = get_length_number(t)
        notes = get_notes(t)
        print(f"Style: {style}\n "
              f"Style Number: {style_number}\n "
              f"Orientation: {orientation}\n "
              f"Length Number: {length}\n "
              f"Notes: {notes}")
        print()


tests = ["BK24R-35R-4_Upper",
         "A1R_lower",
         "b5LLRR",
         "Cs234-58G"]


def main():
    b = Block("WT5R-2_Upper_Left_Outside")
    b.report()


if __name__ == "__main__":
    main()
