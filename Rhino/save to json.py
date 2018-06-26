import json

file = r"C:\Users\mkreidler\Desktop\BVTC-Logo-BLACK-horizontal.txt"
data = ["hello", 12312351235234, "hi"]
gold = ["turkey"]
with open(file, 'w') as outfile:
    json.dump(data, outfile)
    json.dump(data, outfile)