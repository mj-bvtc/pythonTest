import pandas as pd

class block:
    def __init__(self):
        self.name = None
        self.point = None
        self.layer = None
        self.guid = None


blocks = []

for i,g in enumerate(guids):
    b = block()
    b.name = names[i]
    b.point = points[i]
    b.layer = layers[i]
    b.guid = guids[i]
    blocks.append(b)


df = pd.DataFrame([vars(f) for f in blocks])

df = df[["name","guid"]].groupby("name").count().reset_index()
print(df)