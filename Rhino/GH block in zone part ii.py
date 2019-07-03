import pandas as pd
import re


class Block():
    def __init__(self):
        self.guid = None
        self.name = None
        self.point = None
        self.layer = None
        self.zones = None
        self.x = None
        self.y = None
        self.z = None
        self.floor = None
        self.swing_drop = None
        self.elevation = None
        self.priority = None
        self.phase = None
        self.group = None

blocks = []


def find_floor(x):
    pat = r"floor\s*(\d*)"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return int(result.group(1))    

def find_elevation(x):
    pat = r"([a-zA-Z\s]*)\s*ELEVATION"
    result = re.search(pat, str(x), flags=re.IGNORECASE)
    if result:
        return result.group(1)

def get_drop(x):
    pat = r"drop\s*([a-z]*\d*)"
    match = re.search(pat, str(x), flags=re.IGNORECASE)

    if match:
        # print("Found Match")
        return match.group(1)
    else:
        # print("Not Found")
        return None

for i, z in enumerate(block_zones):
    b = Block()
    b.guid = block_guid[i]
    b.name = block_name[i]
    b.point = block_pt[i]
    b.layer = block_layer[i]
    b.zones = z
    b.x = b.point[0]
    b.y = b.point[1]
    b.z = b.point[2]
    b.floor = find_floor(str(z))
    b.elevation = find_elevation(str(z))
    b.swing_drop = get_drop(str(z))

    blocks.append(b)

df = pd.DataFrame([vars(f) for f in blocks])

print(df)

df.to_excel(r"C:\Users\mkreidler\Desktop\test.xlsx")


